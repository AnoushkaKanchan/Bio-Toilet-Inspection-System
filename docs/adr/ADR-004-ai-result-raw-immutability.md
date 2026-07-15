# ADR-004: AIResultRaw Immutability

## Status

Accepted

## Context

The AI service sends inspection results to the backend.

These results represent the exact output produced by the AI model and must be preserved for auditing, replay, debugging, and future reprocessing.

## Decision

`AIResultRaw.payload` is immutable after creation.

- The payload is written exactly once.
- The payload is never modified.
- The Mapping domain may read from `AIResultRaw` but must never mutate it.
- If the AI service generates a new result, a new `AIResultRaw` record is created instead of updating the existing one.

## Consequences

- Preserves the original AI response.
- Supports replaying the Mapping Engine.
- Improves auditability.
- Keeps AI integration separate from railway business logic.