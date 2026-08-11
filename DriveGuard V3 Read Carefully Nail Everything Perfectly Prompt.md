# DRIVEGUARD V3 — READ EVERYTHING CAREFULLY, NO-RUSH, NO-OMISSIONS, NAIL-EVERYTHING DIRECTIVE

This prompt supplements every other DriveGuard prompt supplied in this task.

It exists because this project contains many detailed, overlapping requirements and will likely be implemented across more than one model/session.

Treat this directive as binding throughout the entire build.

---

# 1. READ ALL PROVIDED PROMPTS BEFORE ACTING

Before changing code, read every DriveGuard prompt supplied to you completely.

Do not skim headings.

Do not assume later prompts replace earlier prompts.

Unless two instructions directly conflict, all prompts are cumulative and binding.

Build a requirement map before implementation.

You should understand:

- what the app is
- who the user is
- what the core product promise is
- how navigation should work
- how speed warnings work
- how cameras appear on the map
- how camera relevance is determined
- how signals and restrictions work
- how the UI must look and behave
- how data provenance works
- how testing works
- how the project is deployed

Do not begin writing large amounts of code until you understand the full system.

---

# 2. IT IS BETTER TO BE THOROUGH THAN FAST

Do not optimize for producing the fastest possible visible answer.

Optimize for getting the implementation correct.

Take the time necessary within the active coding session to:

- read
- inspect
- plan
- implement
- compile
- test
- render
- inspect
- fix
- retest

Do not rush because the prompt is long.

Do not reduce scope simply to finish sooner.

Do not give the user fake confidence.

---

# 3. CREATE A MASTER REQUIREMENTS MATRIX

Before implementation, create:

`docs/REQUIREMENTS_MATRIX.md`

Read every supplied prompt and turn its meaningful requirements into rows.

Suggested columns:

```text
Requirement ID
Prompt Source
Requirement
Subsystem
Implementation File/Module
Test
Status
Notes/Blocker
```

Statuses:

- NOT_STARTED
- IN_PROGRESS
- DONE
- BLOCKED_EXTERNAL
- PARTIAL

Do not mark DONE casually.

Use this matrix continuously so requirements are not forgotten.

---

# 4. CREATE A BUILD CHECKLIST

Create:

`docs/BUILD_CHECKLIST.md`

Group by:

- architecture
- mobile
- UI
- navigation
- cameras
- signals
- speed limits
- restricted turns
- Copilot
- enforcement explorer
- backend
- PostGIS
- ingestion
- admin
- community
- challan
- offline
- Android Auto
- CarPlay
- testing
- security
- DevOps
- documentation
- release

Check items only when genuinely implemented.

---

# 5. DO NOT “INTERPRET AWAY” DIFFICULT REQUIREMENTS

If the prompt asks for:

“camera must be direction aware”

do not implement:
“camera within 500 m.”

If the prompt asks for:
“flyover vs surface road”

do not ignore road level.

If the prompt asks for:
“camera visible on map”

do not implement only voice alerts.

If the prompt asks for:
“Google-Maps-like full navigation”

do not produce a generic map screen with no real navigation.

If the prompt asks for:
“real Mumbai data”

do not seed fake Mumbai camera coordinates.

If a requirement is hard, solve it properly or document a real blocker.

---

# 6. NEVER SILENTLY DROP A FEATURE

If a feature cannot be completed because of an external dependency:

mark:

`BLOCKED_EXTERNAL`

and state exactly why.

Examples:

- commercial map provider API key
- provider contract
- Apple entitlement
- signing certificate
- unavailable official data source

But still implement:

- interfaces
- mocks for tests
- UI states
- backend contracts
- documentation

Do not silently omit it.

---

# 7. RESEARCH CURRENT EXTERNAL APIS BEFORE USING THEM

For anything external and current, use official documentation.

Especially:

- Flutter
- Android navigation SDK
- Mappls
- Google Maps / Navigation SDK
- Android background location
- Android Auto
- iOS background location
- CarPlay
- PostGIS
- provider licensing

Do not code from stale memory.

Do not invent package names or methods.

---

# 8. UNDERSTAND LICENSING BEFORE DATA MIXING

Do not assume map-provider content can be mixed freely.

Before overlaying data:

- inspect terms
- determine caching rights
- determine redistribution rights
- determine display restrictions
- document provider profile

If legally uncertain:

isolate source/provider until resolved.

Do not solve licensing by ignoring it.

---

# 9. ARCHITECTURE FIRST, BUT DO NOT STOP THERE

Create architecture and ADRs.

Then immediately implement.

Architecture documents are not the product.

The task is complete only when code works.

---

# 10. BUILD SHARED CONTRACTS EARLY

Freeze:

- data models
- event types
- camera model
- restriction model
- provider interfaces
- API schemas
- alert types
- confidence states

before parallel subagents create incompatible implementations.

---

# 11. IF USING SUBAGENTS, ORCHESTRATE THEM

Do not just launch agents and hope.

Give each subagent:

- scope
- relevant prompt sections
- existing contracts
- files they own
- tests they must add
- definition of done

After each subagent:

review its changes.

Integrate.

Run tests.

---

# 12. CONTEXT HANDOFF BETWEEN MODELS

This project may begin on one model and continue on another.

Therefore maintain durable project memory inside the repo.

At all times keep updated:

- `docs/REQUIREMENTS_MATRIX.md`
- `docs/IMPLEMENTATION_STATUS.md`
- `docs/ARCHITECTURE.md`
- `docs/NAVIGATION_PROVIDER_DECISION.md`
- `docs/UI_UX_SPEC.md`
- `docs/SCREEN_INVENTORY.md`
- `docs/MUMBAI_DATA_COVERAGE.md`
- `docs/KNOWN_BLOCKERS.md`
- `docs/NEXT_ACTIONS.md`

When a model/session ends, update these first.

A new model must be able to continue without re-inventing architecture.

---

# 13. NEVER CLAIM SOMETHING WORKS WITHOUT VERIFYING

Do not say:

“implemented”

without:
- code
- compile
- relevant test
- actual behavior verification where practical

Do not say:
“build passes”
unless command ran successfully.

Do not say:
“camera data loaded”
unless actual records were imported.

Do not say:
“all Mumbai cameras”
unless a valid exhaustive source proves it.

---

# 14. TEST AS YOU BUILD

Do not leave testing until the end.

For every critical module:

- add unit tests
- integration tests
- simulator scenarios
- UI/golden tests where appropriate

Use the exact production compliance logic in simulator.

---

# 15. VISUALLY INSPECT THE UI

UI quality is not proven by widget tests.

For every important screen:

1. run/render
2. screenshot
3. inspect
4. fix
5. rerender

Check:
- spacing
- alignment
- hierarchy
- map visibility
- camera clutter
- dark mode
- safe areas
- small screens
- landscape
- speed/limit readability
- warning overlap

Do not leave ugly default UI.

---

# 16. PAY SPECIAL ATTENTION TO THE CORE USER EXPERIENCE

The critical user flow is:

1. open app
2. see map
3. search destination
4. choose route
5. inspect route intelligence
6. start navigation
7. see turn instructions
8. see current speed
9. see speed limit
10. see cameras on map
11. hear camera warning at relevant distance
12. receive overspeed warning
13. receive restricted-turn warning
14. get rerouted when needed
15. arrive

This flow must be excellent.

Do not prioritize secondary features over this path.

---

# 17. CAMERA BEHAVIOR MUST BE PRECISE

Every camera-related decision must consider, where data permits:

- road segment
- route
- carriageway
- direction
- heading
- road level
- service road
- flyover
- underpass
- monitored lanes
- active state
- verification state
- along-route distance

False alerts destroy trust.

Test opposite-direction and flyover cases repeatedly.

---

# 18. SPEED LIMIT BEHAVIOR MUST BE PRECISE

Never fabricate limit.

If unknown:
say unknown.

Smooth GPS speed.

Use hysteresis.

Do not beep from a single noisy sample.

Camera warning does not replace continuous compliance.

---

# 19. RESTRICTED TURN BEHAVIOR MUST BE PRECISE

No-left/no-right/no-U-turn/no-entry/one-way restrictions must be respected by routing.

If provider route conflicts with verified compliance rule:
detect it.

Do not knowingly route through prohibited movement.

---

# 20. DATA PROVENANCE MUST BE REAL

Every production enforcement/restriction record should have a reason to exist.

Preserve:

- source
- retrieval time
- source record/document
- confidence
- verification
- freshness
- version history

Never use invented production coordinates.

---

# 21. DO NOT HIDE COVERAGE GAPS

If data is incomplete:
show it internally.

Admin dashboard should measure reality.

Documentation should say what is missing.

This is better than fake completeness.

---

# 22. KEEP THE CONSUMER UI SIMPLE

The app may be technically complex.

The UI must not look complex.

Do not put:
- data-source confidence math
- ingestion information
- admin controls
- debugging
- raw geometry

on the normal navigation UI.

Consumer experience:
simple.

Admin:
detailed.

---

# 23. REVIEW PERFORMANCE

Navigation is real-time.

Avoid:

- server call for every GPS sample
- rebuilding huge marker lists every frame
- full Mumbai spatial scans
- excessive re-rendering
- giant API payloads
- repeated TTS messages

Profile and optimize.

---

# 24. REVIEW PRIVACY

Precise location is sensitive.

Before logging or transmitting anything, ask:
“Do we need this?”

Default to minimal retention.

Do not send full driving traces to analytics.

---

# 25. REVIEW SECURITY

Before final completion:
- search secrets
- audit admin roles
- validate uploads
- test rate limits
- inspect auth
- inspect provider key restrictions
- inspect logs for location/PII leakage

---

# 26. REVIEW ALL TODO/FIXME PLACEHOLDERS

Before final report, search entire repo:

```text
TODO
FIXME
HACK
PLACEHOLDER
MOCK
DUMMY
FAKE
NOT_IMPLEMENTED
```

Review each occurrence.

Test-only mocks are okay.

Production placeholders are not.

---

# 27. DO NOT LET MODEL SWITCHES CAUSE REGRESSIONS

When continuing from another model:

1. read repo docs
2. inspect git status/log
3. run existing tests
4. understand current architecture
5. continue

Do not rewrite working modules merely because you would have designed them differently.

Preserve validated contracts unless there is a concrete reason to change them.

---

# 28. COMMIT / MILESTONE DISCIPLINE

If git access exists:

use logical commits.

Examples:
- foundation
- geospatial core
- navigation provider
- UI shell
- camera intelligence
- restriction engine
- admin
- simulator
- QA fixes

Do not produce one giant opaque commit if avoidable.

---

# 29. BEFORE DECLARING DONE, PERFORM A FULL REQUIREMENTS RE-READ

At the end:

re-read EVERY supplied DriveGuard prompt again.

Compare every section against `REQUIREMENTS_MATRIX.md`.

Anything missed:
implement it or mark a genuine blocker.

Do not assume memory captured everything.

---

# 30. FINAL POLISH PASS

After functionality:

do a dedicated polish pass.

UI:
- spacing
- typography
- dark mode
- map clutter
- transitions
- errors
- responsiveness

Code:
- duplication
- naming
- dead code
- lint
- comments
- docs

Data:
- provenance
- stale records
- synthetic separation

Tests:
- flaky tests
- missing critical scenarios

---

# 31. FINAL RELEASE-CANDIDATE LOOP

Run:

1. dependency install
2. format
3. lint
4. type check
5. unit tests
6. integration tests
7. PostGIS tests
8. provider mocks/contracts
9. Flutter tests
10. UI golden tests
11. simulator
12. critical route scenarios
13. admin tests
14. backend build
15. Android build
16. iOS build where environment permits
17. security scans
18. Docker build
19. staging smoke test if possible

Fix failures.

Repeat.

---

# 32. FINAL REPORT MUST BE FACTUAL

Report:

## Fully working
Only things verified.

## Partial
Anything incomplete.

## External blockers
With exact reason.

## Tests
Exact commands/results.

## Data coverage
Real counts/status.

## UI
Screens inspected and known defects.

## Next actions
Only truly remaining work.

Do not use vague confidence language.

---

# 33. THE QUALITY STANDARD

This should not feel like:

“an AI generated a lot of code.”

It should feel like:

“a disciplined engineering team built a polished navigation product.”

The implementation must be coherent across:
- mobile
- backend
- data
- UI
- simulator
- admin
- deployment

---

# 34. PRODUCT NORTH STAR — REPEAT THIS BEFORE MAJOR DECISIONS

A Mumbai driver should be able to replace Google Maps for driving with DriveGuard.

They should get:

- familiar destination search
- reliable route choices
- clean turn-by-turn navigation
- ETA and traffic
- current speed
- current speed limit
- warnings to reduce speed when over the limit
- visible speed cameras on the map
- distance to relevant upcoming cameras
- voice camera alerts
- red-light/signal enforcement awareness
- prohibited-turn/no-entry warnings
- temporary road restrictions
- Copilot Mode if they choose another map app

The UI must remain clean despite all this intelligence.

---

# 35. FINAL DIRECTIVE

Read everything.

Do not rush.

Do not skip.

Do not fake.

Do not guess production road data.

Do not silently reduce scope.

Build methodically.

Verify continually.

Use subagents carefully.

Leave durable documentation so another model can continue.

Re-read requirements before completion.

Fix issues instead of merely documenting them when they are fixable.

It is acceptable for implementation to require a long, careful coding session.

What is not acceptable is declaring success after a shallow implementation.

Nail each subsystem properly.

Nail the UI.

Nail the data model.

Nail camera relevance.

Nail speed-limit behavior.

Nail restricted turns.

Nail the simulator.

Nail the tests.

Nail the integration.

Nail the final polish.

BEGIN BY READING ALL DRIVEGUARD PROMPTS IN FULL, THEN BUILD.
