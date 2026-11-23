def get_travel_advisory(country: str) -> dict:
    """Get the current travel advisory for a country.
    Note: uses mock data — replace with a real government API in production.
    """
    advisory_data = {
        "japan": {
            "safety_level": 1,
            "advisory": "Exercise normal precautions.",
            "entry_requirements": "No visa required for stays under 90 days for most nationalities. Valid passport required.",
        },
        "france": {
            "safety_level": 2,
            "advisory": "Exercise increased caution due to terrorism risk in some areas.",
            "entry_requirements": "EU citizens: national ID sufficient. Others: valid passport required. No visa for Schengen stays under 90 days.",
        },
        "usa": {
            "safety_level": 1,
            "advisory": "Exercise normal precautions.",
            "entry_requirements": "ESTA required for Visa Waiver Program countries. Valid passport required.",
        },
    }
    data = advisory_data.get(
        country.lower(),
        {
            "safety_level": 3,
            "advisory": "Check your government's official travel advisory for this destination.",
            "entry_requirements": "Check visa requirements for your nationality before travelling.",
        },
    )
    result = {"country": country, **data}
    print("~" * 20, f"get_travel_advisory({country!r}) → {result}", "~" * 20)
    return result


travel_advisory_tool_schema = {
    "type": "function",
    "function": {
        "name": "get_travel_advisory",
        "description": "Get the current travel advisory and entry requirements for a country.",
        "parameters": {
            "type": "object",
            "properties": {
                "country": {
                    "type": "string",
                    "description": "The name of the country (e.g. 'Japan', 'France', 'USA').",
                }
            },
            "required": ["country"],
        },
    },
}

tools_with_advisory = tools + [travel_advisory_tool_schema]
tool_registry_with_advisory = {**tool_registry, "get_travel_advisory": get_travel_advisory}

# Test query, once your tool is ready, the agent should use it
test_query = """
I'm planning a trip to Japan next month.
What's the weather in Tokyo, what time is it there now, how much is 300 EUR in Yen,
and is Japan safe to travel to? Any entry requirements I should know about?
"""

messages = [
    {"role": "system", "content": system_prompt},
    {"role": "user", "content": test_query},
]

run_travel_assistant(messages, tools_with_advisory, tool_registry_with_advisory)
