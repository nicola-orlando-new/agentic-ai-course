"""
Solution: Travel agent guardrails, switch on both layers in travel_agent/agent.py

Step 1, prompt guardrails: use SYSTEM_GUARDRAILS instead of SYSTEM as the instruction.
It adds scope, refusal, and security rules, enforced by the model.

Step 2, callback guardrails: input_guardrail and tool_guardrail are already written in
guardrails.py, but nothing calls them until they are imported and registered on the LlmAgent.

- before_model_callback runs before every LLM call. input_guardrail goes here, so a
  prompt-injection message is answered with REFUSAL and the model is never called.
- before_tool_callback runs before every tool call. tool_guardrail goes here, so a
  negative amount for convert_currency is rejected before the tool runs.
"""

# --- UNCOMMENT this import in travel_agent/agent.py (step 2) ---
#
# from .guardrails import input_guardrail, tool_guardrail

# --- CHANGE root_agent = LlmAgent(...) in travel_agent/agent.py ---
#
# root_agent = LlmAgent(
#     name="travel_agent",
#     instruction=SYSTEM_GUARDRAILS,              # step 1
#     ...
#     generate_content_config=types.GenerateContentConfig(
#         temperature=0.1,
#     ),
#     before_model_callback=input_guardrail,      # step 2
#     before_tool_callback=tool_guardrail,        # step 2
# )
