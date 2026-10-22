# Architecture and boundaries

- Put decisions and domain calculations in functions or methods that can run without infrastructure whenever practical.
- Keep adapters such as HTTP, database, filesystem, queue, and external API integrations responsible for decoding inputs, executing effects, and translating outputs.
- Prefer a functional core and imperative shell without enforcing a particular layered architecture.
- Model state transitions explicitly when multiple flags could create contradictory combinations. Use enums, variants, sealed hierarchies, tagged unions, or ordinary domain objects according to language idioms.
- Validate and parse external inputs once at appropriate trust boundaries; revalidate when crossing a genuinely new trust boundary. Treat database values according to the ownership and guarantees of the persistence boundary rather than assuming every database read is equally untrusted.
- Keep transactions and resource ownership with the orchestrator that can guarantee cleanup and consistency.
- Avoid pure-function wrappers that only forward arguments, excessive interface proliferation, and framework rewrites.

## Review questions

- Can domain decisions be tested without external services?
- Is it clear where side effects occur?
- Are invalid states difficult to create without making the model cumbersome?
- Are transaction and resource lifetimes preserved?
