"""Workflow Pattern 2: Parallel - Trip Search Fan-Out.

This exercise shows a fan-out/fan-in workflow. Once the traveler preferences are
known, flights, hotels, and activities can be researched independently. A
JoinNode waits until all three branches finish before the itinerary is composed.

Graph shape:

    START -> Preferences -> (FlightSearch || HotelSearch || Activities) -> Join -> Composer

Try:
    "I'm flying from Amsterdam to Lisbon for 4 days in September with my partner.
    Our total budget is 2000 EUR. We love food, history, and nightlife."
"""

from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm
from google.adk.workflow import START, JoinNode, Workflow

from prompts import (
    ACTIVITY_AGENT_SYSTEM,
    FLIGHT_SEARCH_AGENT_SYSTEM,
    HOTEL_SEARCH_AGENT_SYSTEM,
    ITINERARY_COMPOSER_SYSTEM,
    PREFERENCES_AGENT_SYSTEM,
    STATE_ACTIVITIES,
    STATE_FLIGHTS,
    STATE_HOTELS,
    STATE_ITINERARY,
    STATE_PREFERENCES,
)

MODEL = LiteLlm("gemini/gemini-3.1-flash-lite")


preferences_agent = LlmAgent(
    name="PreferencesAgent",
    model=MODEL,
    instruction=PREFERENCES_AGENT_SYSTEM,
    description="Extracts destination, dates, budget, and interests from the traveler request.",
    output_key=STATE_PREFERENCES,
)

flight_search_agent = LlmAgent(
    name="FlightSearchAgent",
    model=MODEL,
    include_contents="none",
    instruction=FLIGHT_SEARCH_AGENT_SYSTEM,
    description="Creates mock flight options from the extracted preferences.",
    output_key=STATE_FLIGHTS,
)

hotel_search_agent = LlmAgent(
    name="HotelSearchAgent",
    model=MODEL,
    include_contents="none",
    instruction=HOTEL_SEARCH_AGENT_SYSTEM,
    description="Creates mock hotel options from the extracted preferences.",
    output_key=STATE_HOTELS,
)

activity_agent = LlmAgent(
    name="ActivityAgent",
    model=MODEL,
    include_contents="none",
    instruction=ACTIVITY_AGENT_SYSTEM,
    description="Suggests activities that match the traveler's interests.",
    output_key=STATE_ACTIVITIES,
)

search_join = JoinNode(name="SearchJoin")

itinerary_composer_agent = LlmAgent(
    name="ItineraryComposerAgent",
    model=MODEL,
    include_contents="none",
    instruction=ITINERARY_COMPOSER_SYSTEM,
    description="Combines preferences, flights, hotels, and activities into an itinerary.",
    output_key=STATE_ITINERARY,
)


root_agent = Workflow(
    name="WorkflowParallelTripPlanner",
    edges=[
        (START, preferences_agent),
        (preferences_agent, (flight_search_agent, hotel_search_agent, activity_agent)),
        ((flight_search_agent, hotel_search_agent, activity_agent), search_join),
        (search_join, itinerary_composer_agent),
    ],
)
