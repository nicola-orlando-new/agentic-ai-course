# Evaluation

This chapter is designed to fit in one afternoon. The goal is not to build a full evaluation framework from scratch, but to understand the main evaluation patterns and then use ADK's native eval tooling on the travel agent.

## Suggested Flow

1. Start with `01_llm_arena.md` for a short discussion of preference-based evaluation.
2. Run `02_llm_as_a_judge.ipynb` as a compact lab on judge prompts, rubrics, and structured judge outputs.
3. Evaluate the travel agent with ADK's native Eval tab.

The key lesson is simple:

> For normal LLMs, evaluate the answer.
> For agents, evaluate the answer and the actions used to produce it.

In ADK terms, that means comparing both:

- `intermediate_data.tool_uses` with `tool_trajectory_avg_score`
- `final_response` with `final_response_match_v2`

## The Eval Set

The dataset is not defined in a notebook. It lives with the agent:

```text
exercises/01_agents/02_travel_agent/travel_agent/travel_agent_eval.evalset.json
```

ADK discovers any file ending in `.evalset.json` inside an agent package, and the filename minus that suffix becomes the eval set name. Because it is an ordinary file rather than notebook code, the same eval set is read by every entry point:

| Where | How it is used |
|-------|----------------|
| `adk web` → **Eval** tab | Run it by clicking **Start** |
| CI / `adk eval` | Runs headless in a pipeline |
| Python | Loaded with `LocalEvalSetsManager` |

One file, one source of truth. Cases you add in the web UI are immediately visible everywhere else.

It contains 10 cases covering single-tool, multi-tool, efficiency, off-topic refusal, and edge cases, plus two guardrail cases (`eval_guardrail_injection` and `eval_guardrail_negative_amount`) whose reference responses only match once the guardrails from the travel agent exercise are switched on.

## Running It in the Web UI

Start the server as described in the [travel agent README](../01_agents/02_travel_agent/travel_agent/README.md), select **travel_agent**, open the **Eval** tab, pick `travel_agent_eval`, choose your metrics, and click **Start**.

Two metrics are worth enabling first:

| Metric | What it catches |
|--------|-----------------|
| `tool_trajectory_avg_score` | Wrong tool, wrong arguments, missing or duplicated calls |
| `response_match_score` | How many words the final answer shares with the reference response (ROUGE) |

> [!IMPORTANT]
> **Response Match** (`response_match_score`) is ROUGE word overlap: it counts shared words, it does not judge meaning. The reference responses in the eval set are written for a semantic judge, so expect correct answers to fail it.
>
> The Eval tab also lists `final_response_match_v2`, an LLM judge. In this ADK version, the web UI cannot pass it the judge settings it needs, so it shows as *not evaluated*. The LLM-as-a-judge pattern is covered in `02_llm_as_a_judge.ipynb`.
>
> The difference is worth demonstrating live. On `eval_007` the agent answers *"I am sorry, but I do not have the ability to book flights. I can, however, help you with information about Tokyo, such as the current weather, local time, or currency conversion…"* against a reference of *"I can't book flights. I can help with weather, local time, and currency conversion for your trip."* Same refusal, same redirect, and ROUGE scores it around **0.4 to 0.5**, failing a 0.7 threshold. The tool trajectory passes, so the agent behaved correctly, only the wording differs. That gap is the whole argument for LLM-as-a-judge, and it connects straight back to `02_llm_as_a_judge.ipynb`.

> [!NOTE]
> If the Eval tab offers only two metrics, the server could not load the full list. See Troubleshooting in the [travel agent README](../01_agents/02_travel_agent/travel_agent/README.md).

Every run is written to `.adk/eval_history/` inside the agent package, so you can inspect scores after the fact. Click a case in the results to see expected and actual side by side.

## Two Cases to Discuss

**`eval_006` catches a right answer reached the wrong way.** It asks for Tokyo's weather twice in one message, and the eval set expects a single `get_weather` call. With `gemini-3.1-flash-lite` the agent makes one call and the case passes. Switch `agent.py` to `gemini-2.5-flash-lite` and run it again: the agent still answers correctly, but calls `get_weather` twice, so the trajectory fails while the response passes. No response metric can catch that, only the trajectory can. It also shows why you rerun the eval set whenever you change models: the same agent code behaves differently on a different model.

**`eval_009` is a product decision, not a fact.** It asks about "Zorgonia", a city that does not exist. An earlier version of the tools returned plausible fallback values for any unknown city. One model refused without calling a tool, another called the tools and reported made-up weather as if it were real. We decided that the tools should report unknown cities as an error and the agent should pass that on to the user, so the eval set expects calls to `get_weather` and `get_current_time` followed by a reply saying the city could not be found. If you decide on a different behavior, for example refusing before calling any tool, change the expected trajectory and reference response, and the case will start failing until the agent's behavior matches. That is what an eval set is for: it holds your decision in place until the agent catches up.

## Creating Your Own Cases

You can build eval cases from the UI: chat with the agent, then save the session as an eval case.

> [!WARNING]
> A captured case records what the agent **actually did** as what it **should do**. Always review one before trusting it, otherwise you baseline whatever bugs were present at capture time.

## Exercise

After running the eval set once, add three new cases to `travel_agent_eval.evalset.json`. Include one ambiguous query, such as:

```text
What's 100 euros in dollars?
```

Decide whether the correct behavior is to assume USD or ask a clarifying question, then encode that decision in the expected tool trajectory and reference response.

The suggested answer is in:

```text
answers/c02_agent_eval_expand_dataset.py
```
