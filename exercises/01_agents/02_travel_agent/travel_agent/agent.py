from google.adk.agents import LlmAgent
from google.adk.tools import FunctionTool
from google.adk.models.lite_llm import LiteLlm
from dotenv import load_dotenv
from google.genai import types

from .prompts import SYSTEM, SYSTEM_GUARDRAILS
from .tools import get_weather, get_current_time, convert_currency
# Next exercise: after implementing get_travel_advisory in tools.py, add it to this import.
# from .tools import get_travel_advisory
# Guardrails exercise (later), step 2: uncomment this import.
# from .guardrails import input_guardrail, tool_guardrail


load_dotenv()

root_agent = LlmAgent(
    name="travel_agent",
    # Guardrails exercise (later), step 1: switch to the stricter prompt by using SYSTEM_GUARDRAILS here.
    instruction=SYSTEM,
    model=LiteLlm("gemini/gemini-3.1-flash-lite"),
    tools=[
        FunctionTool(get_weather),
        FunctionTool(get_current_time),
        FunctionTool(convert_currency),
        # Next exercise: add FunctionTool(get_travel_advisory) once you've implemented and imported it.
    ],
    generate_content_config=types.GenerateContentConfig(
        temperature=0.1,
    ),
    # Guardrails exercise (later), step 2: register input_guardrail and tool_guardrail as callbacks.
    # Find the LlmAgent parameter that runs before every LLM call, and the one that
    # runs before every tool call, and pass the matching function to each.
    #
    # 💡 Solution available in: answers/c01_n02_travel_agent_guardrails.py
)
