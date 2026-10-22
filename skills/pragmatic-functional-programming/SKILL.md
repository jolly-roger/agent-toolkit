---
name: pragmatic-functional-programming
description: >
  Apply pragmatic functional-programming principles when generating, changing,
  testing, reviewing, or designing code in any language. Improve correctness and
  testability through pure calculations, explicit effects and dependencies,
  immutable boundaries, composition, and clear domain modeling while respecting
  the existing architecture and language conventions.
---
# Pragmatic Functional Programming

Apply this guidance to newly generated code and existing code, including feature implementation, bug fixes, tests, and reviews. Use functional techniques to improve correctness, readability, and testability, not to maximize functional purity. Follow existing architecture and language idioms. Avoid unrelated refactoring.

## Defaults

1. **Pure core, effectful boundaries.** Keep decisions, calculations, and transformations pure where practical. Isolate I/O, persistence, time, randomness, logging, and external calls at understandable boundaries. Do not create wrappers for trivial effects without benefit.
2. **Prefer immutable interfaces.** Do not mutate caller-owned inputs or shared state unexpectedly. Prefer values returned from transformations. Local mutation, in-place algorithms, and framework-managed mutation are fine when clear, safe, or measurably faster.
3. **Explicit dependencies and context.** Make dependencies visible through parameters, constructors, or existing dependency injection. Avoid ambient globals and hidden mutable closure state. Do not pass excessive parameter bundles solely to appear functional.
4. **Compose for clarity.** Favor small cohesive units and readable data flow; use higher-order functions, pipelines, or combinators when they simplify the code. Simple loops and straightforward conditionals are valid.
5. **Model domain constraints.** Represent distinct states clearly using available language types and idioms. Avoid contradictory flags and invalid intermediate states where reasonably preventable. Do not invent complex type machinery for simple problems.
6. **Validate at trust boundaries.** Parse and validate untrusted inputs at API, message, file, and configuration boundaries. Treat database values according to the ownership and guarantees of the persistence boundary. Pass trusted domain values inward where practical and handle malformed data deliberately.
7. **Treat errors intentionally.** Distinguish expected business failures from unexpected defects. Use existing language and project conventions such as exceptions, error returns, or `Result`/`Either`. Do not swallow errors or silently turn failures into successful-looking values. Use an explicit, documented fallback when degradation is intentional. Do not add an FP error library without justification.
8. **Keep behavior deterministic where useful.** Inject clocks, random generators, and other nondeterministic sources when needed for testing. Do not add unnecessary indirection.
9. **Test behavior and invariants.** Favor unit tests for pure logic, boundary and integration tests for effects, and property-based tests when invariants or input spaces warrant them. Preserve existing tests and contracts unless the requested behavior intentionally changes them; update affected tests and contracts when it does.
10. **Respect operational concerns.** Preserve cancellation, resource cleanup, transactions, concurrency bounds, observability, and performance. Do not trade correctness or maintainability for stylistic purity.

## Classification before implementation

Identify **data** (values and facts), **calculations** (deterministic transformations), and **actions** (time-, state-, or world-dependent operations). Keep calculations independent of actions when doing so simplifies the design. An action may coordinate calculations and effects; do not disguise effects as pure functions.

A function is referentially transparent when replacing its invocation with its result does not change observable behavior. Assess hidden state, time, randomness, I/O, mutation, and failure behavior rather than judging purity from syntax alone. A deterministic exception is not the same as an external effect, but it still affects how callers can substitute and compose an expression.

Prefer explicit state transitions such as `nextState = transition(currentState, event)` for domain workflows when practical. Keep effect ordering, retries, and transactional semantics in the orchestrator.

## Decision rules

| Situation | Default | Valid exception |
| --- | --- | --- |
| Business calculation | Pure function | Domain object method already established |
| Update a value | Return updated value | Owned local mutation or performance-sensitive operation |
| I/O workflow | Effectful orchestration around pure decisions | Framework architecture already handles separation |
| Error expected by caller | Explicit, documented failure | Idiomatic exception conventions |
| Complex data flow | Readable composition | Loop is simpler or faster |
| Shared mutable state | Avoid or encapsulate | Necessary synchronized state |
| New abstraction | Introduce only for a concrete benefit | Existing project convention requires it |
| Class vs function | Choose by responsibility and language idiom | Framework-mandated classes |

## Workflow

1. Inspect relevant code, tests, architecture, and local conventions.
2. Classify data, calculations, and actions; identify domain rules, external effects, ownership of mutable state, and failure paths.
3. Choose the smallest implementation consistent with the defaults above.
4. Preserve API contracts, error semantics, and framework lifecycle behavior unless the requested change intentionally updates them.
5. Test success, failure, edge cases, and important invariants.
6. Review the changed diff against the checklist below; do not refactor unrelated code.

## Self-review checklist

- Are domain decisions deterministic and referentially transparent where reasonably possible?
- Are data, calculations, and actions distinguished where useful?
- Are state transitions explicit where they reduce ambiguity?
- Can any mutation unexpectedly affect callers, shared state, or later operations?
- Are external effects and dependencies understandable and testable?
- Are invalid inputs rejected at the right boundary?
- Are domain states and expected failures clear and handled?
- Is composition simpler than the equivalent imperative code?
- Are resource management, concurrency, and performance preserved?
- Are tests focused on observable behavior and relevant invariants?
- Did the change avoid unnecessary FP libraries, abstractions, and unrelated rewrites?

## Deeper guidance

Read only the references relevant to the task:

- [Foundations and decision examples](references/foundations.md) — use for classifying data, calculations, actions, referential transparency, state transitions, and composition tradeoffs.
- [Architecture and boundaries](references/architecture.md) — use when organizing domain logic, adapters, effects, resources, or transactions.
- [Composition and state](references/composition-and-state.md) — use when handling immutable updates, mutable ownership, closures, pipelines, or performance-sensitive transformations.
- [Errors and testing](references/errors-and-testing.md) — use when designing failure behavior, validation, deterministic tests, integration tests, or invariant tests.

When these guidelines conflict, prioritize correctness, explicit user requirements, repository conventions, clarity, testability, and performance over functional purity. Explain a significant tradeoff only when it affects the requested change.
