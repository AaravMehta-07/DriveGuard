# DRIVEGUARD V3 — QA, REAL-WORLD VALIDATION, SIMULATION & RELEASE-GATE PROMPT

This prompt supplements all existing DriveGuard build specifications.

Your job is not merely to make DriveGuard compile.

Your job is to attempt to break it before users do.

Navigation/compliance applications can lose user trust immediately through:

- incorrect camera warning
- wrong speed limit
- wrong-direction camera
- false flyover warning
- illegal route maneuver
- missing restriction
- excessive alerts
- GPS snapping errors

Testing must therefore be unusually thorough.

# 1. BUILD A COMPLETE QA STRATEGY

Testing layers:

```text
Unit
 ↓
Integration
 ↓
Provider Contract
 ↓
Geospatial
 ↓
GPS Simulation
 ↓
Golden Routes
 ↓
Mobile UI
 ↓
End-to-End
 ↓
Field Testing
 ↓
Release Gate
```

# 2. GPS REPLAY ENGINE

Build a reusable GPS simulator capable of replaying:

- GPX
- JSON traces
- synthetic road traces

Controls:

- playback speed
- acceleration
- pauses
- heading
- GPS accuracy
- noise
- location jumps
- signal dropout
- route deviation

It must feed the SAME production live-compliance engine used by the mobile app.

Do not create a separate simplified simulator logic.

# 3. SYNTHETIC ROAD WORLD

Create a deterministic synthetic city map containing:

- divided highway
- surface road
- flyover
- underpass
- service road
- intersections
- no-left
- no-right
- no-U-turn
- one-way
- no-entry
- timed restriction
- speed zones
- speed cameras
- red-light cameras
- normal signals
- camera on opposite carriageway
- camera under flyover

Use this for automated testing.

# 4. CAMERA TEST MATRIX

Test:

### Same road, same direction
Alert.

### Same road, opposite direction
No alert.

### Parallel carriageway
No alert unless applies.

### Nearby service road
No alert.

### Surface camera while on flyover
No alert.

### Flyover camera while on surface
No alert.

### Camera behind vehicle
No alert.

### Camera ahead after U-turn
Re-evaluate correctly.

### Removed camera
No active warning.

### Stale/uncertain camera
Follow confidence policy.

### Multiple cameras close together
No repeated audio chaos.

# 5. DISTANCE TESTS

Verify along-route distance.

Camera 100 m Euclidean but 700 m along road:

display approximately 700 m.

No straight-line shortcut.

# 6. SPEED TEST MATRIX

Test:

- below limit
- exactly at limit
- slight overspeed
- sustained overspeed
- single GPS speed spike
- noisy GPS
- sudden limit reduction
- sudden limit increase
- speed limit unknown
- conditional limit
- offline limit data

Use hysteresis.

# 7. RESTRICTED TURN TEST MATRIX

Test:

- no left
- no right
- no U-turn
- no entry
- one way
- timed restriction active
- timed restriction inactive
- vehicle-specific
- temporary order

Navigation should not route into a verified prohibition.

# 8. ROUTE PROVIDER CONFLICT

Simulate navigation provider suggesting a movement that DriveGuard compliance data says is prohibited.

DriveGuard must detect conflict.

Required behavior:

- prevent/override maneuver where architecture permits
- compute alternative compliant route
- never silently instruct illegal turn

# 9. SIGNAL TESTS

Test:

- ordinary signal
- red-light enforcement
- combined speed/red-light
- signal on adjacent road
- signal on flyover/surface mismatch
- live timer available
- live timer unavailable

Never display fabricated timer.

# 10. ALERT PRIORITY

Test simultaneous:

restricted turn + camera + overspeed.

Expected:

restricted movement dominant.

Speed secondary if important.

Camera tertiary.

Only one major voice message at a time.

# 11. ALERT DEDUPLICATION

Verify same camera does not trigger:

700 m
600 m
500 m
400 m

as four full voice messages.

Use staged policy.

# 12. STATIONARY TRAFFIC

Vehicle stationary near camera for five minutes.

Do not repeatedly warn.

# 13. GPS DRIFT

Simulate dense urban canyon.

Location oscillates between parallel roads.

System should:

- track match confidence
- avoid rapid camera alert flip-flop
- avoid fake speed-limit changes

# 14. LOCATION DROPOUT

Lose GPS for:

- 2 seconds
- 10 seconds
- 30 seconds
- tunnel

UI should degrade gracefully.

Do not manufacture location.

# 15. NETWORK DROPOUT

During navigation:

disable network.

Verify locally cached compliance continues.

Navigation provider behavior should degrade appropriately.

No crash.

# 16. PROVIDER OUTAGE

Mock:

- routing failure
- search failure
- tiles failure
- traffic failure

App should present useful state.

# 17. API QUOTA

Mock quota exceeded.

Do not infinite-retry.

Do not burn requests.

# 18. BATTERY / BACKGROUND

Test Android:

- app foreground
- screen off
- background
- another map app foreground
- foreground service
- process recreation

Verify Copilot survives as intended within platform rules.

Test iOS equivalent permitted cases.

# 19. PERMISSION TESTS

Test:

- precise location granted
- approximate location only
- denied
- background denied
- notifications denied
- permission revoked mid-drive

No crashes.

# 20. MOBILE LIFECYCLE

Test:

- phone call
- app minimize
- rotate
- screen lock
- unlock
- low memory
- process restore

# 21. UI GOLDEN TESTS

Capture stable synthetic screenshots for:

Home day
Home night
Search
Route selection
Navigation
Camera approaching
Overspeed
Restricted left
Signal enforcement
Copilot
Camera explorer
Camera detail
Offline
Settings

Visual regression.

# 22. SMALL SCREEN

Verify minimum target width.

No:

- clipped ETA
- hidden speed
- camera card overlapping route
- maneuver text overflow

# 23. LARGE SCREEN

Avoid enormous wasted components.

# 24. LANDSCAPE

Verify navigation remains usable.

# 25. ACCESSIBILITY

Test:

- large text
- screen reader
- high contrast
- reduced motion

Critical warning understandable without color.

# 26. CAMERA MAP LOAD

Stress test camera visualization.

Test:

100
500
1,000
5,000 candidates in viewport backend query scenarios.

Client should receive only appropriate subset/clusters.

# 27. POSTGIS PERFORMANCE

Benchmark:

- nearby camera
- route corridor intersection
- active temporal restrictions
- directional filtering
- coverage dashboard

Add indexes where needed.

# 28. LOAD TEST BACKEND

Test reasonable concurrent traffic for launch assumptions.

Endpoints:

- route scan
- enforcement viewport
- report submission
- offline metadata
- search proxy if applicable

# 29. INGESTION TESTS

For official notices:

test:

- valid document
- duplicate
- updated version
- malformed PDF/text
- ambiguous road
- expired restriction
- conflicting restriction
- model extraction failure
- geocoder failure

No corrupt production records.

# 30. LLM FAILURE

Mock nonsensical LLM output.

Schema validation must reject.

# 31. ADMIN TESTS

Verify:

approve candidate
reject
merge
edit geometry
change direction
expire restriction
view audit history

# 32. COMMUNITY ABUSE

Simulate malicious user submitting hundreds of cameras.

Rate-limit/block.

Nothing becomes verified automatically.

# 33. CHALLAN PRIVACY TEST

Upload challan containing:

- name
- registration
- address

Verify privacy pipeline redacts/deletes sensitive fields as designed.

# 34. SECURITY TESTS

Run:

- dependency scans
- static analysis
- secret scanning
- API auth tests
- admin RBAC
- upload validation
- malicious file tests
- rate-limit tests

# 35. REAL MUMBAI GOLDEN ROUTES

Where verified source data exists, create real-world regression scenarios for representative Mumbai areas.

Potential categories:

- South Mumbai complex intersections
- Marine Drive
- Western Express Highway
- Eastern Express Highway
- BKC
- major flyovers
- service-road segments

Do not invent legal restrictions.

Real scenario must cite internal source evidence.

# 36. FIELD TESTING

Create safe real-world test plan.

Testers must obey road rules.

Recommended:

driver focuses entirely on driving.

Passenger validates alerts/logging.

Never deliberately overspeed or take illegal turn.

# 37. FIELD TEST METRICS

Measure:

- correct camera alerts
- false camera alerts
- missed known cameras
- wrong-direction alerts
- wrong-road alerts
- speed-limit correctness
- turn restriction correctness
- GPS match accuracy
- audio timing
- alert usefulness
- UI readability

# 38. FALSE POSITIVE TARGET

Minimize false positives aggressively.

A missed low-confidence report is often less damaging than repeatedly warning about nonexistent cameras.

# 39. ISSUE PRIORITIES

P0:
- illegal navigation instruction
- crash during navigation
- dangerously wrong compliance warning
- severe privacy/security issue

P1:
- wrong camera carriageway
- significant speed-limit error
- background navigation failure
- map matching errors

P2:
- UI clutter
- timing issue
- minor provider errors

P3:
- cosmetic

# 40. RELEASE BLOCKERS

Do not ship production if unresolved:

- P0
- major P1 affecting common routes
- fake production data
- broken background service
- provider licensing uncertainty
- exposed secrets
- unverified release build

# 41. MUMBAI LAUNCH GATE

Create:

`docs/MUMBAI_LAUNCH_READINESS.md`

Actual metrics:

```text
App stability
Navigation provider readiness
Camera coverage
Camera verification rate
Signal coverage
Speed limit coverage
Turn-restriction coverage
Temporary notice freshness
False-positive rate
Field tests completed
Known critical gaps
```

# 42. AUTOMATED RELEASE GATE

CI should block release on:

- failing critical unit tests
- migration failure
- compliance regression
- secrets
- lint/type errors
- release build failure

# 43. CRASH MONITORING

Integrate crash reporting.

Tag:

- app version
- navigation provider
- compliance dataset version

Do not attach raw trip traces by default.

# 44. POST-RELEASE TELEMETRY

Measure:

- crash-free navigation sessions
- camera alert confirmation
- incorrect camera reports
- map-match confidence
- battery complaints
- routing failures

Privacy preserving.

# 45. BUG REPRODUCTION

For consented tester sessions:

save enough diagnostic information to replay:

- timestamp
- sanitized GPS
- matched road
- event ID
- dataset version
- alert decision

Use simulator to reproduce.

# 46. DATASET REGRESSION

When camera/rule dataset changes:

rerun relevant route scenarios.

A data update can break behavior even without code change.

# 47. PROVIDER SDK UPDATE GATE

Do not automatically deploy new navigation SDK.

Run:

- builds
- navigation simulator
- route tests
- UI tests

# 48. FINAL QA REPORT

Generate:

`docs/QA_REPORT.md`

Include factual:

- tests executed
- total passed
- failed
- skipped
- performance
- known defects
- blockers

# 49. NO FAKE PASS

Do not write:

“All tests pass”

unless they actually ran.

If environment prevents one:

state it.

# 50. ITERATE

After first complete test pass:

fix issues.

Run again.

Continue until critical suite is green or only genuine external blockers remain.

The objective is a DriveGuard build that is not merely impressive in a demo, but robust enough to survive real Mumbai driving conditions.

BEGIN QA.
