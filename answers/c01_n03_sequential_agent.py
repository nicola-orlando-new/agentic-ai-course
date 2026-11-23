"""
Solution: Sequential, add a packing-list stage

Change: Add a sixth LlmAgent to the workflow_sequential graph that reads the final
{itinerary} and {preferences} from state and writes a packing list.

Define the prompt + state key in prompts.py and the agent in workflow_sequential/agent.py,
then append one edge so the new node runs after the itinerary composer.
"""

from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm

MODEL = LiteLlm("gemini/gemini-3.1-flash-lite")

# --- NEW: add to prompts.py ---
STATE_PACKING_LIST = "packing_list"

PACKING_LIST_AGENT_SYSTEM = """
You are a Travel Packing Assistant.

**Traveler preferences:**
{preferences}

**Final itinerary:**
{itinerary}

**Task:**
Based on the destination, dates, planned activities, and likely weather, produce a practical
packing list grouped into: Documents, Clothing, Toiletries, Electronics, and Activity-specific.
Keep it concise, a few bullet points per group.

Output *only* the packing list.
""".strip()

# --- NEW: add to workflow_sequential/agent.py ---
packing_list_agent = LlmAgent(
    name="PackingListAgent",
    model=MODEL,
    include_contents="none",  # reads {itinerary} and {preferences} from state
    instruction=PACKING_LIST_AGENT_SYSTEM,
    description="Produces a packing list from the final itinerary and preferences.",
    output_key=STATE_PACKING_LIST,
)

# --- Wire it in: append one edge to the Workflow, after the composer ---
#
# root_agent = Workflow(
#     name="WorkflowSequentialTripPlanner",
#     edges=[
#         (START, preferences_agent),
#         (preferences_agent, flight_search_agent),
#         (flight_search_agent, hotel_search_agent),
#         (hotel_search_agent, activity_agent),
#         (activity_agent, itinerary_composer_agent),
#         (itinerary_composer_agent, packing_list_agent),   # <-- added sixth stage
#     ],
# )
