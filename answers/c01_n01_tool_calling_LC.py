
from langchain_community.tools import DuckDuckGoSearchRun

search_tool = DuckDuckGoSearchRun()


@tool
def get_local_highlights(city: str) -> str:
    """Search the web for top attractions, local food, and cultural tips for a city.

    Use this when the user wants recommendations on what to see, eat, or do at a destination.

    Args:
        city: The name of the city (e.g. 'Tokyo', 'Rome').
    """
    query = f"top things to do, local food, and cultural tips in {city}"
    result = search_tool.invoke(query)
    print("~" * 20, f"get_local_highlights({city!r}) -> searched: {query!r}", "~" * 20)
    return result


tools_with_highlights = tools + [get_local_highlights]

highlights_system_prompt = """
You are a helpful travel assistant.
Use the available tools to fetch current information. Never rely on your own knowledge for weather, time, or exchange rates.
For recommendations on sights, food, or culture, use the search tool and summarize what it returns.
"""

#Remember that now we now how to use create_agent
agent_with_highlights = create_agent(
    model=model,
    tools=tools_with_highlights,
    system_prompt=highlights_system_prompt,
)

test_query = """
I'm planning a trip to Japan next month.
What's the weather in Tokyo, what time is it there now, how much is 300 EUR in Yen,
and what are some local highlights, food and sights, I shouldn't miss in Tokyo?
"""

# The followign loop stream the result to see each step:

printed = 0
for step in agent_with_highlights.stream(
    {"messages": [{"role": "user", "content": test_query}]},
    stream_mode="values",
):
    for msg in step["messages"][printed:]:
        msg.pretty_print()
    printed = len(step["messages"])