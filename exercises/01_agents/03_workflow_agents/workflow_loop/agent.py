"""Workflow Pattern 3: Loop - Budget Refinement.

Iterative refinement until the reviewer approves:
  ItineraryPlanner <-> BudgetReviewer (approved == True or max 3 iterations)

The reviewer returns structured output (BudgetReview) with a binary pass/fail
and written feedback. The planner reads the review and revises the itinerary.
loop_gate checks the approval state and exits the loop without a tool call.

A small capture_request node saves the user message to state first: nodes inside
the loop only see their predecessor's output, so both agents read the traveler
request from state via the {user_request} placeholder on every iteration.

Graph shape:

    START -> CaptureRequest -> ItineraryPlanner -> BudgetReviewer -> loop_gate -> finish
                                    ^                                    |
                                    +------------- REFINE --------------+

Try:
    "Plan a luxury 3-night trip to Rome for 2 people. Our budget is 500 EUR."
"""

from google.adk.agents import Context, LlmAgent
from google.adk.agents.callback_context import CallbackContext
from google.adk.events import Event, EventActions
from google.adk.models.lite_llm import LiteLlm
from google.adk.workflow import DEFAULT_ROUTE, START, Workflow, node
from pydantic import BaseModel

from prompts import STATE_BUDGET_REVIEW, STATE_ITINERARY

MODEL = LiteLlm("gemini/gemini-3.1-flash-lite")
STATE_USER_REQUEST = "user_request"


# ---------------------------------------------------------------------------
# Capture request node
# ---------------------------------------------------------------------------
@node
def capture_request(ctx: Context, node_input=None) -> str:
    """Saves the traveler's message to state so both agents can read it every iteration."""
    parts = getattr(node_input, "parts", None) or []
    ctx.state[STATE_USER_REQUEST] = " ".join(part.text for part in parts if part.text)
    return "Planning your trip..."


# ---------------------------------------------------------------------------
# Itinerary planner agent
# ---------------------------------------------------------------------------
def init_state(callback_context: CallbackContext) -> None:
    """Seed budget_review so the {budget_review} template variable exists on iteration 1."""
    callback_context.state.setdefault(STATE_BUDGET_REVIEW, {"approved": False, "feedback": ""})


itinerary_planner_agent = LlmAgent(
    name="ItineraryPlanner",
    model=MODEL,
    include_contents="none",
    instruction=(
        "You are a Travel Itinerary Planner.\n\n"
        "Traveler request:\n{user_request}\n\n"
        "Write a short day-by-day itinerary for this trip.\n\n"
        "If there is budget reviewer feedback below, revise the itinerary to address it:\n"
        "{budget_review}\n\n"
        "Rules:\n"
        "- Keep the traveler's destination and trip length.\n"
        "- Plan the style of trip the traveler asked for (luxury means nice hotels, "
        "restaurants, and paid activities) and price every item realistically.\n"
        "- Never shrink prices just to fit the budget. Only cut costs by making the "
        "specific changes the reviewer feedback asks for.\n"
        "- Give each line item a simple EUR amount.\n"
        "- End with exactly one line: \"Estimated total cost: <amount> EUR\".\n\n"
        "Output only the itinerary."
    ),
    description="Writes or revises a trip itinerary from budget feedback.",
    before_agent_callback=init_state,
    output_key=STATE_ITINERARY,
)


# ---------------------------------------------------------------------------
# Budget reviewer agent
# ---------------------------------------------------------------------------
class BudgetReview(BaseModel):
    approved: bool
    feedback: str


budget_reviewer_agent = LlmAgent(
    name="BudgetReviewer",
    model=MODEL,
    include_contents="none",
    instruction=(
        "You are a strict travel budget reviewer.\n\n"
        "Traveler request (includes the budget):\n{user_request}\n\n"
        "Itinerary to review:\n{itinerary}\n\n"
        "Set approved to true only if the estimated total cost is less than or equal to "
        "the traveler's budget.\n"
        "In feedback, say how far over budget the plan is and give concrete ways to cut "
        "cost — e.g. \"choose a cheaper hotel\", \"drop the most expensive activity\"."
    ),
    description="Checks whether the itinerary fits the budget; returns structured BudgetReview.",
    output_schema=BudgetReview,
    output_key=STATE_BUDGET_REVIEW,
)


# ---------------------------------------------------------------------------
# Loop gate
# ---------------------------------------------------------------------------
def loop_gate(ctx: Context):
    """Checks budget_review in session state and exits the loop if approved.

    No LLM call, no tool call — pure Python logic. Runs after the reviewer
    on every iteration.
    """
    max_iterations: int = 3

    current_iteration = ctx.session.state.get("current_loop_iteration", 1)

    # Get approval information from the reviewer agent
    review = ctx.session.state.get(STATE_BUDGET_REVIEW)
    approved = review.get("approved", False)

    # Exit the loop if the reviewer approved, or we reach the max number of iterations
    exit_loop = approved or (current_iteration >= max_iterations)

    if not exit_loop:
        next_iteration = current_iteration + 1
        yield Event(actions=EventActions(route="REFINE", state_delta={"current_loop_iteration": next_iteration}))
    # On exit we emit no route, so the workflow follows the DEFAULT_ROUTE edge to finish.


@node
def finish(ctx: Context) -> str:
    """Closes the loop with a short status message."""
    review = ctx.state.get(STATE_BUDGET_REVIEW) or {}
    if review.get("approved"):
        return "Done! The itinerary fits the budget."
    return "Done! Stopped after the maximum number of refinement passes."


root_agent = Workflow(
    name="WorkflowLoopTripPlanner",
    edges=[
        (START, capture_request),
        (capture_request, itinerary_planner_agent),
        (itinerary_planner_agent, budget_reviewer_agent),
        (budget_reviewer_agent, loop_gate),
        (loop_gate, {
            "REFINE": itinerary_planner_agent,
            DEFAULT_ROUTE: finish,
        })
    ],
)
