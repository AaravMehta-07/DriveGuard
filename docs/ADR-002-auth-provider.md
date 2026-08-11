# ADR-002: Authentication Provider

**Status**: ACCEPTED

## Context
Evaluate Firebase Auth vs Supabase Auth vs Auth0 for mobile and web client authentication.

## Criteria
- Flutter SDK quality
- Guest/anonymous support
- Token validation simplicity
- Pricing
- Data residency
- Account deletion support

## Decision
**Firebase Auth** is recommended as the default. It provides the best Flutter integration out-of-the-box, has a generous free tier, and strong support for anonymous (guest) authentication flows.

## Consequences
- Backend needs to validate Firebase JWTs.
- Need to implement a flow to link anonymous accounts to permanent credentials.
