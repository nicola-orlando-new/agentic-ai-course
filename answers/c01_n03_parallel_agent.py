"""
Solution: Parallel, add a fourth search branch (car rentals)

Change: Add a CarRentalSearchAgent to the fan-out in workflow_parallel so flights,
hotels, activities, and cars are all searched concurrently. Route the new branch
through the JoinNode, then update the ItineraryComposerAgent prompt to factor car
rentals into the plan and the total.

Define the prompt + state key in prompts.py and the agent in workflow_parallel/agent.py.
"""

from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm

MODEL = LiteLlm("gemini/gemini-3.1-flash-lite")

# --- NEW: add to prompts.py ---
STATE_CARS = "car_options"

CAR_RENTAL_SEARCH_AGENT_SYSTEM = """
You are a Car Rental Search Agent.

**Trip preferences:**
{preferences}

Based on the destination and dates above, return THREE realistic car rental options.
For each option include: rental company, car category (e.g. economy, SUV), price per day,
and total price for the whole trip (match the traveler's currency).

Note: these are mock results for a training exercise, invent plausible values; do not call a real API.

Output *only* the list of three car rental options.
""".strip()

# --- NEW: add to workflow_parallel/agent.py ---
car_rental_search_agent = LlmAgent(
    name="CarRentalSearchAgent",
    model=MODEL,
    include_contents="none",  # reads {preferences} from state
    instruction=CAR_RENTAL_SEARCH_AGENT_SYSTEM,
    description="Returns mock car rental options for the trip.",
    output_key=STATE_CARS,
)

# --- Wire it in: add the branch to the fan-out and the JoinNode ---
#
# root_agent = Workflow(
#     name="WorkflowParallelTripPlanner",
#     edges=[
#         (START, preferences_agent),
#         (preferences_agent, (flight_search_agent, hotel_search_agent, activity_agent, car_rental_search_agent)),
#         ((flight_search_agent, hotel_search_agent, activity_agent, car_rental_search_agent), search_join),
#         (search_join, itinerary_composer_agent),
#     ],
# )
#
# The JoinNode still fires the composer exactly once, now after all FOUR branches finish.
#
# --- Then update ITINERARY_COMPOSER_SYSTEM in prompts.py ---
# Add a "**Car rental options:**\n{car_options}" section to the inputs, and instruct the
# composer to optionally include a car rental and add its cost to the estimated total.
