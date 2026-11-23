"""
Solution: Travel Agent Eval - Expand the Eval Set

Three new cases for the travel agent eval set. Ids continue from eval_010, the
highest already in the file.

The dataset is not defined in a notebook. Add these to:

    exercises/01_agents/02_travel_agent/travel_agent/travel_agent_eval.evalset.json

Two ways to do it:

1. Paste the JSON below into the "eval_cases" list in that file, then re-run the
   eval from the ADK web Eval tab.
2. Recreate them in the ADK web Eval tab: ask the agent each question, save the
   session as an eval case, then correct the captured trajectory and reference.

Either way the README workflow and the web UI both use the same eval set file.

The third case is the ambiguous one the exercise asks for: it names no explicit
currency codes, so the agent has to resolve "euros" -> EUR and "dollars" -> USD
on its own.
"""

NEW_CASES = """
{
  "eval_id": "eval_011",
  "conversation": [
    {
      "invocation_id": "eval_011",
      "user_content": {
        "parts": [{"text": "I land in Lisbon tomorrow. What's the weather there, and what time is it now?"}],
        "role": "user"
      },
      "final_response": {
        "parts": [{"text": "Lisbon is clear with a temperature of 20 C and 50% humidity. The answer should also include the local time returned by the tool, with UTC+0."}],
        "role": "model"
      },
      "intermediate_data": {
        "tool_uses": [
          {"args": {"city": "Lisbon"}, "name": "get_weather"},
          {"args": {"city": "Lisbon"}, "name": "get_current_time"}
        ],
        "tool_responses": [],
        "intermediate_responses": []
      }
    }
  ],
  "final_session_state": {}
},
{
  "eval_id": "eval_012",
  "conversation": [
    {
      "invocation_id": "eval_012",
      "user_content": {
        "parts": [{"text": "Is it raining in Amsterdam right now?"}],
        "role": "user"
      },
      "final_response": {
        "parts": [{"text": "No, it is not raining in Amsterdam right now. It is clear and 20 C."}],
        "role": "model"
      },
      "intermediate_data": {
        "tool_uses": [
          {"args": {"city": "Amsterdam"}, "name": "get_weather"}
        ],
        "tool_responses": [],
        "intermediate_responses": []
      }
    }
  ],
  "final_session_state": {}
},
{
  "eval_id": "eval_013",
  "conversation": [
    {
      "invocation_id": "eval_013",
      "user_content": {
        "parts": [{"text": "What's 100 euros in dollars?"}],
        "role": "user"
      },
      "final_response": {
        "parts": [{"text": "100 EUR is about 117.0 USD."}],
        "role": "model"
      },
      "intermediate_data": {
        "tool_uses": [
          {"args": {"amount": 100, "from_currency": "EUR", "to_currency": "USD"}, "name": "convert_currency"}
        ],
        "tool_responses": [],
        "intermediate_responses": []
      }
    }
  ],
  "final_session_state": {}
}
"""

# --- What to look for when you re-run ---
#
# Lisbon and Amsterdam are NOT in the mock data.
#
# Look at get_weather in tools.py: unknown cities fall through to a default of
# 20 C, "Clear", 50% humidity, and get_current_time falls back to UTC+0. So the
# tool returns plausible-looking data for any city, and the agent reports it as
# fact with no hedging. That is why the reference responses above say 20 C and
# clear rather than real Lisbon or Amsterdam weather.
#
# This is worth pausing on. The trajectory is perfect, the response matches the
# reference, both metrics pass - and the user was still told something false.
# Neither tool_trajectory_avg_score nor final_response_match_v2 can see it,
# because neither one knows what the tool *should* have returned. Silent
# fallbacks inside a tool are invisible to reference-based evaluation.
#
# Contrast this with eval_009 (Zorgonia), where the agent refuses because the
# city is obviously invented. "Lisbon" is a real city, so nothing looks wrong.
#
# eval_013 is the ambiguity case. The agent silently resolves "dollars" to USD
# and answers 117.0. The trajectory metric checks the exact arguments, so it
# would catch a wrong currency code - but it cannot tell you whether assuming
# was the right call in the first place. That is a product decision you have to
# encode.
#
# If you decide clarification is correct instead, change the case to:
#
#     "tool_uses": []
#
# and make the reference response a clarifying question, for example:
#
#     "Dollars could mean USD, AUD, or CAD. Which one did you mean?"
#
# The case will then fail until the agent's behaviour matches, which is exactly
# what an eval set is for: it holds your decision in place until the agent
# catches up.
