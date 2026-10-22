# Composition and state

- Prefer explicit input/output transformations over unexpected mutation of arguments.
- Consider copy-on-write, immutable records, or new collections for externally observable values.
- Allow local mutable accumulators and loops when they are simpler than chains of allocations or combinators.
- Closures over mutable values are stateful even when the function signature looks pure; examine captured variables.
- Favor cohesive functions with meaningful names; do not split functions only to minimize line count.
- Use map/filter/fold/pipe or partial application only when the resulting flow is easier to read and debug.
- Be aware that currying and partial-application argument order affect readability; avoid clever point-free expressions.
- Respect object identity, ORM tracking, UI framework state ownership, and concurrency semantics.

## Review questions

- Who owns each mutable value?
- Could a caller observe unexpected changes?
- Does composition clarify intent or hide control flow?
- Is a simple imperative implementation clearer?
