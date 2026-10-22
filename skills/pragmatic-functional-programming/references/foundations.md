# Functional foundations and decision examples

## Actions, calculations, and data

- **Data:** values representing facts or state. Keep ownership and validity clear.
- **Calculations:** deterministic transformations of explicit inputs, with no externally observable effects. Prefer them for domain rules.
- **Actions:** operations whose outcome or effects depend on time, external state, or interaction with the world, including I/O, logging, persistence, randomness, and clocks. Place them at understandable boundaries and orchestrate calculations within them.

For example, instead of a pricing function that fetches discounts and mutates an order, fetch the discount in an effectful coordinator, compute a new priced order with a pure calculation, then persist it. Do not force extra layers when the workflow is trivial.

## Referential transparency

A call is referentially transparent if it can be replaced by its result without changing observable program behavior. Watch for hidden mutation, captured state, clocks, random values, I/O, and failure behavior. An immutable return value does not alone make a function pure. A deterministic exception differs from an external effect, but callers still need its failure behavior to be explicit enough for safe composition.

## State transitions

Prefer `newState = transition(oldState, event)` when it makes domain behavior explicit and testable. Validate allowed transitions and handle invalid events deliberately. For concurrent state changes, preserve locking, transactions, ordering, and idempotency.

## Composition and transformation

Prefer readable sequences of named transformations when they clarify intent. Use loops where they are clearer, avoid repeated full collection copies in hot paths, and avoid pipelines that obscure errors or execution order.

## Sources and scope

These principles are synthesized from Eric Normand, *Grokking Simplicity*; Scott Wlaschin, *Domain Modeling Made Functional*; Pilquist, Bjarnason, and Chiusano, *Functional Programming in Scala*, second edition; and Vermeulen, Bjarnason, and Chiusano, *Functional Programming in Kotlin*. They are conceptual references, not language-specific requirements.
