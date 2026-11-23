"""
Solution: Loop, tighten the budget check with a 10% safety buffer

Change: Make the BudgetReviewer stricter so it only approves when the estimated total
leaves at least a 10% buffer under the budget. This makes the loop run more refinement
passes before it exits (and shows why the max-pass cap matters).

The reviewer in workflow_loop/agent.py returns structured output (BudgetReview with an
`approved` bool), so only its instruction changes, no changes to the graph or the gate,
which already reruns the reviewer each pass.
"""

# --- REPLACE the instruction= on budget_reviewer_agent in workflow_loop/agent.py ---
#
# budget_reviewer_agent = LlmAgent(
#     name="BudgetReviewer",
#     model=MODEL,
#     include_contents="none",
#     instruction=(
BUDGET_REVIEWER_INSTRUCTION = (
    "You are a strict travel budget reviewer.\n\n"
    "Traveler request (includes the budget):\n{user_request}\n\n"
    "Itinerary to review:\n{itinerary}\n\n"
    "Require a SAFETY BUFFER: set approved to true only if the estimated total cost is "
    "at most 90% of the traveler's budget (leaving at least 10% unspent for incidentals).\n"
    "In feedback, say how far over the 90% threshold the plan is and give concrete ways "
    "to cut cost, e.g. \"choose a cheaper hotel\", \"drop the most expensive activity\"."
)
#     ),
#     description="Checks whether the itinerary fits the budget; returns structured BudgetReview.",
#     output_schema=BudgetReview,
#     output_key=STATE_BUDGET_REVIEW,
# )

# Note: with a stricter reviewer, the planner will usually need to trim costs on the first
# pass or two before it approves. If it can't get under 90% within the max number of passes,
# the loop stops anyway and returns the best itinerary so far (loop_gate routes to `finish`),
# which is exactly why the iteration cap exists.
