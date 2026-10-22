# Errors and testing

- Distinguish expected domain failures such as not found, invalid transition, or insufficient balance from programming defects and infrastructure faults.
- Follow the codebase's established error conventions. Use `Result`/`Either`, return values, or exceptions when each is idiomatic; avoid introducing a new error framework for stylistic reasons.
- Do not swallow errors or silently convert them into successful-looking defaults. An explicit, documented fallback is valid when graceful degradation is part of the required behavior.
- Decode and validate untrusted input at the boundary, then operate on trusted values where possible.
- Test pure business logic using representative examples and edge cases.
- Consider property-based tests for stable invariants such as conservation, idempotence, ordering, reversibility, and round trips when relevant.
- Use integration tests for persistence, networking, retries, cancellation, resource cleanup, and transactions.
- Use deterministic fakes or injected clock and randomness sources when nondeterminism otherwise makes tests fragile.
- Preserve existing tests and contracts unless requested behavior changes them. When it does, update the affected expectations deliberately instead of weakening unrelated coverage.

## Review questions

- Are all meaningful failure modes handled or propagated?
- Are boundary errors actionable?
- Are invariant tests worth their complexity?
- Does the test suite cover the real effects, not only pure helpers?
