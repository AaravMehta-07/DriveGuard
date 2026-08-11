# API Versioning Strategy

## Prefix
All API routes must be prefixed with `/api/v1/`.

## Semantic Versioning
- Major versions (v1, v2) for breaking changes.
- Minor/patch handled transparently, no breaking changes permitted within a major version.

## Backward Compatibility Policy
- Additions are allowed (new endpoints, new optional fields).
- Removals or required field changes require a new major version.

## Deprecation Policy
- Deprecated endpoints must return a `Warning` header.
- Deprecation must be announced 3 months prior to removal.
