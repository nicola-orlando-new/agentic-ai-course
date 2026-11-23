# Workflow Agents, Trip Planner

This exercise teaches the three orchestration patterns from Google's Agent Development Kit (ADK), **sequential**, **parallel**, and **loop**, using the graph-based `Workflow` API (`google.adk.workflow`).

You get **four** agents built around the same travel-planning task:

| Agent (in the `adk web` picker) | Pattern | What it shows |
|---|---|---|
| `workflow_sequential` | Sequential | Five stages run strictly in order, each reading the previous stage's output from state. |
| `workflow_parallel` | Parallel | Flights, hotels, and activities are searched concurrently, then joined before composing. |
| `workflow_loop` | Loop | An itinerary is refined against the traveler's budget until it fits (or hits a max pass count). |
| `trip_planner_workflow` | All three, composed | The full pipeline, sequential backbone, a parallel search stage, and a refinement loop, plus a conversational front door. |

Start with the three single-pattern agents to learn each shape in isolation, then look at `trip_planner_workflow` as a showcase of how the pieces compose. You do not need to memorize that full file; read it after the smaller examples to see the patterns working together in one graph.

Minimum path through this exercise:

1. Run `workflow_sequential` and inspect only `workflow_sequential/agent.py`.
2. Run `workflow_parallel` and compare how the fan-out plus `JoinNode` differs from the chain.
3. Run `workflow_loop` and focus on the budget gate plus the back-edge.
4. Open `trip_planner_workflow/agent.py` last, once the three smaller patterns feel familiar.

`trip_planner_workflow` still stops at a finalized itinerary. The next production step would be adding user confirmation and booking tools after `finalize`.

## Prerequisites

Make sure your environment is set up and your `GEMINI_API_KEY` is available (see the root [README](../../../README.md)).

## Running the agents

From the root of the repository, run:

```bash
uv run adk web --allow_origins="*" exercises/01_agents/03_workflow_agents --reload_agents
```

This starts a local web server at `http://localhost:8000`. Pick any of the four agents from the dropdown, send it a message, and watch each node execute in the events panel.

**Try the sequential and parallel agents with:**

> *"I'm flying from Amsterdam to Lisbon for 4 days in September with my partner. Our total budget is 2000 EUR. We love food, history, and a bit of nightlife."*

**Try the loop agent with a deliberately tight budget** (so you can watch it refine over several passes):

> *"Plan a luxury 3-night trip to Rome for 2 people. Our budget is 500 EUR."*

---

## Reading guide

Read the code in the same order you run the agents. For each file, start with the `edges=[...]` list: that is the workflow graph. Then look at the agent definitions above it to see which prompts and state keys each node uses.

| File | First-pass focus | Skip on first pass |
|---|---|---|
| `workflow_sequential/agent.py` | The straight chain of edges from `START` to the composer | Prompt details in `prompts.py` |
| `workflow_parallel/agent.py` | The fan-out from preferences to the three search agents, then the `JoinNode` | The exact mock search wording |
| `workflow_loop/agent.py` | The budget review gate and the back-edge to the planner | Fine details of the refinement prompt |
| `trip_planner_workflow/agent.py` | The full `edges=[...]` list and how the three patterns compose | Intake routing, custom node internals, and state-capture details |

On the first pass through `trip_planner_workflow/agent.py`, it is enough to understand the graph shape. Come back to `IntakeGate`, `BudgetGate`, and `capture_request` after the smaller examples make sense.

## The three patterns as graphs

In the `Workflow` API, each pattern is **graph structure**, nodes connected by edges, rather than a wrapper class. `LlmAgent`s drop straight into the edge list: each one reads its inputs from **shared session state** (via `{placeholder}` injection in its prompt) and writes its result to an `output_key` that later nodes read.

**Sequential**, a straight chain of edges:

```
START → Preferences → FlightSearch → HotelSearch → Activities → Composer
```

**Parallel**, a fan-out to independent branches, joined before the next stage. A `JoinNode` is required: a plain node with multiple incoming edges would fire once per predecessor, so the join waits for all branches and fires the composer exactly once.

```
START → Preferences → (FlightSearch ‖ HotelSearch ‖ Activities) → Join → Composer
```

**Loop**, a conditional route plus a back-edge. A small non-LLM gate reads the reviewer's verdict from state and either routes back to the planner (`REFINE`) or falls through the default edge to finish:

```
START → CaptureRequest → ItineraryPlanner → BudgetReviewer → loop_gate → finish
                              ▲                                   │
                              └────────────── REFINE ─────────────┘
```

The shared prompts and state keys for all four agents live in [`prompts.py`](prompts.py).

> **Why a gate instead of an `exit_loop` tool?** A natural first instinct is to give the planner an `exit_loop` tool and let the model call it when the reviewer approves. In practice that's flaky with Gemini via LiteLlm: the model sometimes emits the tool call as plain *text* (polluting state), and a turn that calls a tool with no text trips ADK 2.4's `MODEL_RETURNED_NO_CONTENT` error. A tiny non-LLM gate that reads the verdict from state and routes in plain Python is deterministic and reliable, and capping the loop with a state counter guards against a plan that never fits.

> **Note on the mock data:** the flight/hotel/activity agents *invent* plausible results from their prompts, there's no real API behind them. In a production system you'd swap in real search tools (as `FunctionTool`s or an MCP server, like in notebooks 02 and 04).

---

## A note on the older shell-agent classes

Earlier ADK versions expressed these same patterns with one wrapper class each, `SequentialAgent`, `ParallelAgent`, and `LoopAgent`. Those classes are **deprecated in ADK 2.4** in favour of the graph-based `Workflow` API and print a `DeprecationWarning` when instantiated, so this exercise uses `Workflow` throughout.

The mapping is worth keeping in mind if you meet the old classes elsewhere:

| Pattern | Deprecated shell agent | `Workflow` graph |
|---|---|---|
| Sequential | `SequentialAgent(sub_agents=[…])` | a chain of edges: `a → b → c` |
| Parallel | `ParallelAgent(sub_agents=[…])` | fan-out `a → (b, c)` + a `JoinNode` to wait for both |
| Loop | `LoopAgent(…)` + an escalate signal | a conditional route `{"refine": …, DEFAULT_ROUTE: …}` + a back-edge |

`Workflow` is more powerful (arbitrary graphs, conditional routing, joins, a deterministic gate replacing the `exit_loop` tool) but also more verbose. The `trip_planner_workflow` agent also adds a **conversational front door** the single-pattern agents don't have: an intake classifier and gate greet the user and explain what the assistant can do, and only run the planning flow once a real trip request arrives.

> **Workflow gotcha worth knowing:** a Workflow node only sees its *predecessor's* output, not the original user turn (unlike a `SequentialAgent`, which shares the whole conversation). So the graph captures the user's message into state at the start (`capture_request`) and the entry agents read it via `{user_request}` with `include_contents="none"`. Without that, downstream agents hallucinate default values.

---

## Extra challenges

Once the agents run, try extending them. Solutions are in the [`answers/`](../../../answers/) folder, files prefixed `c01_n03_`.

Do the **sequential** challenge below, it is the one to complete in this session. The parallel and loop challenges are there if you finish early or want to keep going afterwards.

### Sequential, add a packing-list stage *(the challenge)*
Add a `PackingListAgent` as a **sixth** node at the end of the `workflow_sequential` chain. It should read the final `{itinerary}` and `{preferences}` from state and produce a packing list, writing to `output_key="packing_list"`.
This is an append-only change: add the prompt/state key, define the new agent, and add one final edge after the composer.
→ [`c01_n03_sequential_agent.py`](../../../answers/c01_n03_sequential_agent.py)

### Parallel, add a fourth search branch *(if you finish early)*
Add a `CarRentalSearchAgent` to the fan-out in `workflow_parallel` (writing to `output_key="car_options"`), wire it through the `JoinNode`, and update the `ItineraryComposerAgent` prompt to consider car rentals in the plan and the total cost.
You will update both `prompts.py` and `workflow_parallel/agent.py`.
→ [`c01_n03_parallel_agent.py`](../../../answers/c01_n03_parallel_agent.py)

### Loop, tighten the budget check *(if you finish early)*
Make the budget reviewer stricter: only approve when the estimated total leaves a **10% safety buffer** under the budget. Observe how the loop now runs more refinement passes (and why the max-pass cap matters).
Only the reviewer instruction needs to change; the graph edges and `loop_gate` stay the same.
→ [`c01_n03_loop_agent.py`](../../../answers/c01_n03_loop_agent.py)
