# Add this function to mcp_servers/travel_mcp_server.py, then restart the server.

@mcp.tool
def get_travel_advisory(country: str) -> dict:
    """Get the current travel advisory for a country.

    Args:
        country: The name of the country (e.g. 'Japan', 'Italy').

    Returns:
        A dict with safety_level (1-5), advisory, and entry_requirements.

    Note:
        Uses mock data — replace with a real government API in production.
    """
    advisory_data = {
        "japan": {
            "safety_level": 1,
            "advisory": "Exercise normal precautions.",
            "entry_requirements": "No visa required for stays under 90 days for most nationalities. Valid passport required.",
        },
        "italy": {
            "safety_level": 1,
            "advisory": "Exercise normal precautions.",
            "entry_requirements": "EU citizens: national ID sufficient. Others: valid passport required. No visa for Schengen stays under 90 days.",
        },
        "usa": {
            "safety_level": 1,
            "advisory": "Exercise normal precautions.",
            "entry_requirements": "ESTA required for Visa Waiver Program countries. Valid passport required.",
        },
    }
    return {"country": country, **advisory_data.get(
        country.lower(),
        {
            "safety_level": 3,
            "advisory": "Check your government's official travel advisory for this destination.",
            "entry_requirements": "Check visa requirements for your nationality before travelling.",
        },
    )}
