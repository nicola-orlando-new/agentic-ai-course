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
        "italy": {
            "safety_level": 1,
            "advisory": "Exercise normal precautions.",
            "entry_requirements": "EU citizens: national ID sufficient. Non-EU: valid passport required. No visa for stays under 90 days (Schengen).",
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
    return {"country": country, **data}
