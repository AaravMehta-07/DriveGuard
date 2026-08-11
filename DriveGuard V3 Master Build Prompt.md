# MASTER BUILD PROMPT — DRIVEGUARD V3
## Production-Grade India-First Navigation + Traffic-Compliance + Enforcement Intelligence Platform

You are the **principal architect, lead engineer, product engineer, geospatial engineer, mobile engineer, backend engineer, QA lead, DevOps engineer, security engineer, data engineer and implementation orchestrator** for this project.

Your job is to build the complete application described below.

Do not merely create a prototype, UI mockup, architecture document, skeleton repository, or partial proof of concept.

Build the actual working system.

The working product name is:

# DriveGuard

Treat the name and branding as replaceable configuration so it can be renamed later without architectural changes.

---

# 0. PRIMARY OBJECTIVE

Build a production-grade mobile navigation application initially optimized for:

**Mumbai, Maharashtra, India**

with architecture capable of expanding to:

Mumbai → MMR → Maharashtra → India → other countries.

DriveGuard should be usable **instead of Google Maps for driving navigation**.

The core value proposition is:

> A clean, familiar navigation application that helps drivers obey speed limits, understand road restrictions, avoid accidentally making prohibited turns or entering restricted roads, and remain aware of verified speed/red-light enforcement infrastructure.

The application must combine:

- complete turn-by-turn navigation
- destination search
- route selection
- live traffic where provider-supported
- rerouting
- current speed
- applicable speed limit
- speed-limit changes
- speed warnings
- speed-camera locations
- red-light camera locations
- combined enforcement cameras
- traffic-signal locations
- turn restrictions
- no-entry roads
- one-way rules
- no-U-turn rules
- time-dependent restrictions
- vehicle restrictions
- temporary traffic-police orders
- closures
- parking restrictions
- challan/enforcement hotspots
- route compliance scanning
- community reports
- offline compliance cache
- Android Auto
- CarPlay architecture
- Android/iOS support
- background “Copilot Mode”
- administrative data-verification tools
- government-notice ingestion
- multi-source enforcement-data ingestion
- route/GPS simulation
- comprehensive automated tests

The app must be **useful, clean, fast and visually familiar to Google Maps users**, but it must NOT make a pixel-perfect copy of Google Maps or infringe Google branding/trade dress.

Use familiar navigation interaction patterns while giving DriveGuard an independent visual design.

---

# 1. NON-NEGOTIABLE PRODUCT RULES

## 1.1 Full navigation

DriveGuard must provide:

Search destination → choose route → preview route → start → turn-by-turn navigation → arrival.

The user should not need Google Maps.

## 1.2 Copilot Mode

Also provide a secondary mode called:

**DriveGuard Copilot**

The user can tap:

**Start DriveGuard**

without entering a destination.

The application then follows the vehicle using GPS and provides:

- current road
- current speed
- speed limit
- speeding warnings
- relevant upcoming enforcement cameras
- traffic-signal enforcement
- prohibited movements
- no-entry warnings
- temporary restrictions
- road closures
- applicable compliance alerts

This mode should continue appropriately when the user switches to another navigation application, subject to Android/iOS platform restrictions and permissions.

---

# 2. CRITICAL SAFETY / ETHICAL PRODUCT PRINCIPLE

DriveGuard is NOT an application for defeating enforcement.

The application must encourage users to follow road rules throughout their journey.

Camera warnings must supplement continuous speed-limit compliance.

The application must NEVER communicate:

“you can speed until the next camera.”

Instead:

- continuously display speed limit
- warn when significantly above the limit
- additionally show upcoming enforcement
- clearly communicate that posted signs and directions from authorities take precedence

UI/legal copy should say essentially:

> DriveGuard provides navigation and road-compliance assistance using available data. Road conditions and restrictions can change. Always follow posted traffic signs, signals and directions from authorities.

Never claim:

“Guaranteed no challans.”

Use terms such as:

- compliance assistance
- verified restrictions
- route intelligence
- enforcement awareness
- route confidence

---

# 3. ABSOLUTE DATA-INTEGRITY RULE

## NEVER FABRICATE REAL-WORLD ROAD DATA.

This is one of the most important instructions in this entire project.

You MUST NOT create fictional:

- speed-camera coordinates
- signal-camera coordinates
- speed limits
- road restrictions
- traffic-signal coordinates
- temporary traffic orders
- camera directions
- road geometry
- official notices
- enforcement types
- verification counts

just to make the application appear complete.

If complete real data cannot be legally/API-accessibly acquired automatically, build the complete acquisition/import/verification system and clearly expose coverage gaps.

Synthetic data may ONLY exist in:

- development fixtures
- automated tests
- simulations

and must be unmistakably marked `synthetic=true`.

Production data must include provenance.

---

# 4. MUMBAI ENFORCEMENT COVERAGE GOAL

DriveGuard should attempt to build the highest-quality legally obtainable database of known Mumbai:

- fixed speed cameras
- red-light cameras
- combined speed/red-light cameras
- other verified automated enforcement points
- average-speed enforcement zones where applicable
- speed-limit zones
- traffic signals
- stop lines
- restricted turns
- one-way roads
- no-entry roads
- no-U-turn locations
- time-dependent restrictions
- road closures
- temporary traffic-police orders
- reverse-lane arrangements
- vehicle-specific restrictions
- heavy-vehicle restrictions
- parking restrictions
- known enforcement/challan hotspots

Every sufficiently verified camera must be **visible geographically on the DriveGuard map**.

The user must be able to browse cameras even when not navigating.

---

# 5. CAMERA MAP — MANDATORY

The main map must contain an Enforcement layer.

Camera icons must be shown geographically.

Possible visual types:

- fixed speed camera
- red-light camera
- combined red-light + speed camera
- average-speed zone
- traffic-monitoring camera
- reported/unverified camera
- verified enforcement camera

Do NOT label ordinary CCTV cameras as enforcement cameras unless their enforcement purpose is verified.

Camera icons should cluster at low zoom.

Example:

`Camera cluster: 12`

Tapping expands/zooms to individual locations.

At closer zoom, show individual camera markers.

---

# 6. CAMERA DETAILS

Tapping an enforcement camera should show a compact bottom sheet containing relevant verified information:

- enforcement type
- road name
- carriageway/direction
- applicable speed limit if known
- monitored lanes if known
- verified/probable/unverified status
- data confidence
- source category
- last verification date
- user-confirmation count
- temporary/permanent status
- direction arrow on map if known

Do not expose unnecessary sensitive infrastructure information beyond what is lawful and appropriate.

---

# 7. CAMERA DATA MODEL

Every enforcement point should support fields conceptually equivalent to:

```text
id
type
geometry
latitude
longitude
road_segment_id
road_level
carriageway
travel_direction
direction_tolerance
monitored_lanes
speed_limit_kph
speed_limit_source
active_status
permanent_or_mobile
source_id
source_type
confidence_score
first_observed_at
last_verified_at
last_source_sync_at
verification_count
contradiction_count
evidence_metadata
synthetic
created_at
updated_at
```

Use PostGIS geometry rather than treating location only as raw lat/lng.

---

# 8. DIRECTION-AWARE CAMERA WARNINGS

A camera being geographically close is NOT sufficient to alert the driver.

An enforcement alert must consider:

- matched current road segment
- route
- travel direction
- camera monitored direction
- carriageway
- road level
- flyover vs surface road
- parallel/service road
- underpass
- distance along road
- vehicle movement
- speed
- camera type
- confidence
- active status

Example:

A speed camera is 70 metres away geographically but monitors the opposite carriageway.

Result:

- camera may remain visible on map
- NO voice alert

Another example:

The user is driving on a flyover while a camera is on the surface road beneath.

Result:

- NO irrelevant warning

This requirement is critical in Mumbai.

---

# 9. CAMERA APPROACH DISTANCE

Do not use naive straight-line distance for warnings.

Compute approach distance along:

- route geometry, or
- matched road graph in Copilot Mode.

Use adaptive alert distances according to speed and context.

Implement a configurable algorithm rather than hard-coded arbitrary values.

Conceptually:

slow urban road → shorter warning distance

faster arterial/highway → longer warning distance

Warnings should give sufficient reaction time while avoiding excessive noise.

Example experience:

> “Speed camera ahead in 700 metres. Speed limit 50 kilometres per hour.”

Later:

> “Speed enforcement ahead. Limit 50.”

If the user is already compliant, do not repeatedly nag them.

If significantly overspeeding:

> “Reduce speed. Limit 50.”

---

# 10. CAMERA ROUTE TIMELINE

During navigation provide a collapsible panel:

## Upcoming

Example:

```text
📷 0.6 km     Speed camera · 50
🚦 1.4 km     Traffic signal
🚦📷 2.0 km   Signal enforcement
🚫 2.7 km     Restricted left
60  3.8 km    Speed limit changes
📷 5.2 km     Speed camera · 60
```

Only relevant route events belong here.

The default collapsed driving UI must remain clean.

---

# 11. ROUTE SCANNER

Before navigation starts, automatically scan each candidate route.

Show:

## Route Intelligence

Example:

```text
6 speed cameras
2 signal-enforcement points
1 restricted movement
4 speed-limit changes
0 current known closures
98% route compliance-data coverage
```

These values MUST be computed.

Never fabricate them.

Provide:

**Show on Map**

Highlight relevant enforcement/restrictions along the route.

---

# 12. ROUTE CHOICES

Offer normal useful routes such as:

- Recommended
- Fastest
- Alternative

And where data quality allows:

## DriveGuard Route

A route optimized to minimize uncertain/complex compliance situations without unreasonable detours.

Do NOT intentionally route around police enforcement so users can violate rules.

Instead optimize for:

- verified legal maneuvers
- reliable road data
- fewer ambiguous restrictions
- reduced risk of accidental prohibited movements
- closures
- vehicle restrictions

---

# 13. ROUTE COMPLIANCE CONFIDENCE

Calculate a route-data-confidence score.

Example:

`Route intelligence coverage: 97%`

Base this on:

- portion of route with verified speed data
- known turn restrictions
- temporary order freshness
- signal/enforcement coverage
- source quality
- unresolved contradictions
- stale records

Never show “100% safe from challans.”

---

# 14. ILLEGAL-TURN PREVENTION — SIGNATURE FEATURE

This is one of the highest-priority DriveGuard features.

DriveGuard must prevent the exact kind of situation where a driver takes an innocent-looking prohibited left/right turn and receives a challan.

Represent:

- no left turn
- no right turn
- no U-turn
- one-way
- no entry
- conditional turn restrictions
- vehicle-class restrictions
- time-dependent restrictions

The routing engine must never intentionally plan an illegal maneuver according to active verified rules.

Before every navigation maneuver:

```text
proposed navigation maneuver
        ↓
ComplianceEngine.validateManeuver()
        ↓
allowed / prohibited / uncertain
```

If prohibited:

- reject the maneuver
- route around it

If uncertain:

- choose a better verified alternative when reasonable
- otherwise clearly flag uncertainty

---

# 15. PROACTIVE TURN WARNING

If approaching a restricted movement:

At an appropriate distance:

> “Restricted left turn ahead.”

Closer:

> “Do not take the next left. Continue straight.”

Visual warning should temporarily become prominent.

Example:

```text
🚫
DO NOT TAKE
NEXT LEFT

Restricted movement
120 m
```

Do not keep full-screen warnings longer than necessary.

---

# 16. COPILOT TURN PREDICTION

When no route exists, use:

- current segment
- heading
- recent trajectory
- junction geometry
- movement possibilities
- road graph

to identify dangerous/prohibited upcoming movements.

Avoid pretending to know the driver’s intent too early.

Warn when trajectory/maneuver likelihood becomes sufficiently high or when a restricted entry is directly ahead.

---

# 17. SPEED LIMIT SYSTEM

Always support:

- current speed
- applicable speed limit
- unknown-speed-limit state
- upcoming limit changes
- conditional speed limits
- direction-specific limits
- vehicle-specific limits where relevant

Driving UI example:

```text
┌─────┐
│ 50  │
└─────┘
LIMIT

47 km/h
```

If speed-limit information is uncertain:

display appropriately instead of inventing a value.

---

# 18. SPEED WARNING LOGIC

Implement configurable severity levels.

Conceptually:

- within reasonable GPS tolerance → no warning
- slightly above limit → subtle visual warning
- consistently/significantly above → stronger visual warning
- substantial overspeed → voice/haptic warning

Account for GPS noise.

Avoid warnings caused by one noisy location sample.

Use hysteresis/debouncing.

Do not create distracting continuous audio.

---

# 19. SPEED-LIMIT CHANGE ALERT

Example:

> “Speed limit changes to 40 ahead.”

Show the upcoming change on the route.

When the vehicle enters the new segment, update speed-limit UI immediately after reliable map matching.

---

# 20. TRAFFIC SIGNAL INTELLIGENCE

Signals must be treated as first-class map entities.

Represent traffic-signal junctions including where data is available:

```text
junction
approaches
stop_lines
traffic_signal_heads
lane movements
permitted movements
restricted movements
red-light enforcement
speed enforcement
signal phase source
signal countdown source
confidence
```

Normal signal:

`🚦`

Verified red-light enforcement:

`🚦 + camera`

Combined enforcement:

distinct appropriate marker.

---

# 21. LIVE SIGNAL TIMERS

If a licensed/current provider legitimately exposes real-time signal countdown/phase data and use is permitted:

support it.

If not available:

DO NOT estimate or fabricate signal countdowns.

The UI must make a clear distinction between:

- live verified signal data
- static signal location
- unavailable phase data

---

# 22. NAVIGATION HOME SCREEN

Use a full-screen map.

Top floating search field:

**Where to?**

Support:

- text search
- POI search
- addresses
- landmarks
- businesses
- autocomplete
- voice search if platform permissions allow
- recent destinations
- favorites
- Home
- Work

Primary secondary action:

**Start DriveGuard**

for Copilot Mode.

Camera/signal markers may already be visible according to selected layers.

---

# 23. ROUTE-SELECTION UI

After destination selection:

- show destination
- show route lines
- show traffic if provider supports it
- show alternatives
- ETA
- distance
- estimated arrival
- toll information if provider supports it
- route intelligence summary
- route scanner
- Preview button
- Start button

Keep it visually clean.

---

# 24. DRIVING UI

Use a minimal, distraction-aware interface.

Essential elements:

TOP:
- next maneuver icon
- distance to maneuver
- road name/instruction

MAP:
- route
- vehicle position
- upcoming enforcement icons
- relevant traffic signals
- selected compliance markers
- lane guidance where available

LOWER LEFT:
- speed limit
- current speed

LOWER/CONTEXT:
- next important DriveGuard warning

BOTTOM:
- ETA
- remaining distance
- estimated arrival

Controls:
- recenter
- overview
- mute/unmute
- report
- layers only when safe/appropriate

No dashboard overload.

---

# 25. VISUAL DESIGN PRINCIPLES

The interface should feel immediately understandable to users familiar with:

- Google Maps
- Apple Maps
- Waze

but maintain original DriveGuard branding.

Requirements:

- clean
- spacious
- minimal
- modern
- legible while mounted in a car
- large touch targets
- excellent day/night modes
- high contrast
- accessibility
- minimal animation while driving
- no unnecessary text
- voice-first warnings
- clear icon semantics

Do not copy proprietary Google UI assets or exact visual arrangement.

---

# 26. DAY / NIGHT MODE

Provide:

- system mode
- automatic navigation night mode
- manual light
- manual dark

Driving UI must remain easily readable at night without excessive brightness.

---

# 27. MAP LAYERS

Provide one simple layers interface.

Default useful layers:

- Traffic
- Speed cameras
- Signal enforcement
- Traffic signals
- Restricted turns
- No-entry
- Community reports

Optional:

- Challan hotspots
- Parking restrictions
- Temporary restrictions
- road closures
- speed-limit layer
- unverified reports

Use sensible defaults.

Avoid turning Mumbai into an unreadable icon field.

---

# 28. ENFORCEMENT EXPLORER

Create a dedicated:

## Mumbai Enforcement Map

Users can browse known enforcement points without starting navigation.

Filters:

- All
- Speed
- Red light
- Combined
- Average-speed
- Verified
- Reported
- signals
- restrictions

Provide search.

Map should support clustering.

---

# 29. DATA-PROVIDER ARCHITECTURE

Do not tightly bind business logic to one maps company.

Create provider abstractions.

Conceptually:

```text
MapProvider
SearchProvider
GeocodingProvider
RoutingProvider
NavigationProvider
TrafficProvider
SpeedLimitProvider
SignalProvider
EnforcementProvider
RoadGraphProvider
```

Potential providers may include, depending on current capabilities/licensing:

- Mappls
- Google Maps Platform
- OpenStreetMap-derived provider
- internal DriveGuard datasets
- government sources

At build time, research CURRENT official SDK/API documentation and terms.

Do not depend on stale assumptions.

---

# 30. PROVIDER ISOLATION / LICENSING

This is critical.

Do not illegally combine provider content.

Before implementation, inspect current official terms for every provider.

For example, if a provider prohibits:

- using its routing information on another company’s map
- mixing its search content with another map
- persistently storing restricted provider data

then design around those restrictions.

Implement:

`ProviderProfile`

Example conceptual profiles:

```text
MAPPLS_FULL
GOOGLE_FULL
OSM_DEV
```

Each profile defines a legally coherent combination of:

- map renderer
- search
- routing
- navigation
- provider-owned traffic information

DriveGuard’s own independently sourced compliance database may only be layered where licensing allows.

Document every provider/legal constraint in:

`docs/provider-licensing.md`

Do not bypass API terms.

---

# 31. PROVIDER SELECTION RESEARCH

Before settling the production default:

evaluate Mappls and Google specifically for:

- Mumbai POI/search quality
- lane guidance
- flyovers/service roads
- routing
- live traffic
- navigation SDK maturity
- speed-limit availability
- traffic-signal support
- camera support
- Flutter/native integration
- background navigation
- offline capabilities
- pricing
- storage restrictions
- commercial terms
- Android Auto compatibility
- iOS compatibility

Implement adapters so switching provider does not rewrite DriveGuard's compliance engine.

Document the decision in an ADR.

---

# 32. OPENSTREETMAP

Use OSM where technically and legally appropriate for:

- road graph
- one-way tags
- turn restrictions
- maxspeed
- traffic signals
- conditional restrictions
- enforcement relations
- road geometry

Respect ODbL and attribution/share-alike obligations.

Do not import incompatible data into an OSM-derived database without verifying licensing compatibility.

Create clear provenance boundaries.

---

# 33. MUMBAI TRAFFIC POLICE INGESTION

Build an ingestion pipeline for official Mumbai Traffic Police public notices and relevant official traffic orders.

The pipeline must discover new official documents/notices related to:

- no entry
- one way
- road closure
- alternative route
- reverse lane
- no parking
- parking restrictions
- heavy-vehicle restrictions
- temporary traffic management
- special-event restrictions
- route changes
- other relevant traffic orders

Pipeline:

```text
Official source monitor
        ↓
new notice detected
        ↓
download/fetch document
        ↓
extract text
        ↓
structured LLM extraction
        ↓
geocode named roads/landmarks
        ↓
match against road graph
        ↓
confidence calculation
        ↓
automated validation
        ↓
admin review if needed
        ↓
publish verified rule
```

Ingestion must be:

- idempotent
- auditable
- retryable
- timestamped
- source-linked
- versioned

Do not silently overwrite past restrictions.

---

# 34. LLM DOCUMENT EXTRACTION

Use an LLM only for extraction/interpretation.

Define strict structured schemas.

Extract:

- notice number
- authority
- publication date
- effective start
- effective end
- “until further order”
- roads
- endpoints
- junctions
- direction
- restriction type
- vehicle class
- exceptions
- time of day
- days of week
- alternative routes
- source text spans
- confidence

Store source evidence.

LLM output NEVER directly becomes production road law without deterministic validation/confidence gating.

---

# 35. NEVER USE LLM IN LIVE SAFETY LOOP

During driving:

DO NOT ask an LLM:

“Is this turn legal?”

The live engine must be deterministic and local/low-latency.

LLMs are allowed for:

- notice extraction
- challan extraction
- source reconciliation
- moderation assistance
- admin suggestions
- data QA

NOT:

- live movement legality
- live speed determination
- immediate camera relevance
- route safety decision

---

# 36. ROAD COMPLIANCE GRAPH

Create a dedicated compliance model.

Support:

```text
SPEED_LIMIT
SPEED_CAMERA
RED_LIGHT_CAMERA
COMBINED_CAMERA
AVERAGE_SPEED_ZONE
TRAFFIC_SIGNAL
NO_LEFT_TURN
NO_RIGHT_TURN
NO_U_TURN
NO_ENTRY
ONE_WAY
REVERSE_LANE
ROAD_CLOSED
LANE_CLOSED
TEMPORARY_RESTRICTION
VEHICLE_RESTRICTION
HEAVY_VEHICLE_RESTRICTION
TIME_RESTRICTION
NO_PARKING
NO_STOPPING
ODD_EVEN_PARKING
BUS_LANE
TOLL
SCHOOL_ZONE
PEDESTRIAN_ZONE
COMMUNITY_REPORT
CHALLAN_HOTSPOT
```

Rules must support:

- geometry
- road segment
- approach
- direction
- time
- date
- days
- vehicle types
- exceptions
- source
- confidence
- version

---

# 37. VEHICLE PROFILES

Support at least:

- private car
- taxi
- motorcycle
- commercial vehicle
- heavy vehicle

Private car should be default for initial consumer launch.

Rules may apply differently according to vehicle class.

Allow user to save multiple vehicles.

Never require registration number unless a feature genuinely requires it.

---

# 38. MAP MATCHING

Create a robust location/map-matching layer.

Inputs:

- GPS
- accuracy
- speed
- bearing
- recent trajectory
- route
- candidate road segments
- road class
- road level

Output:

```text
MatchedPosition {
  roadSegmentId
  positionAlongSegment
  heading
  confidence
  roadLevel
  carriageway
}
```

Handle GPS drift.

Avoid snapping a car on a flyover to the road underneath.

---

# 39. ALERT ENGINE

Create one centralized Alert Engine.

Severity:

```text
P0 CRITICAL
P1 HIGH
P2 MEDIUM
P3 INFORMATIONAL
```

Example priorities:

P0:
- prohibited immediate maneuver
- entering no-entry/wrong-way road
- major road closure

P1:
- substantial overspeed
- imminent active restriction

P2:
- upcoming enforcement
- speed-limit change

P3:
- informational signal
- community report

Implement arbitration.

Do not allow three alerts to speak simultaneously.

Deduplicate.

Apply cooldowns.

Choose the highest-priority useful message.

---

# 40. VOICE GUIDANCE

Use natural concise prompts.

Examples:

> “Speed camera ahead in 600 metres. Limit 50.”

> “Restricted left turn ahead.”

> “Do not take the next left. Continue straight.”

> “Speed limit changes to 40.”

> “Signal enforcement ahead.”

Allow:

- voice on/off
- alerts-only
- full navigation voice
- volume control where appropriate

Use platform TTS or licensed provider voice guidance.

---

# 41. HAPTICS

Use subtle haptics for:

- serious speed warning
- prohibited maneuver warning
- major route-compliance warning

Do not vibrate constantly.

---

# 42. COMMUNITY REPORTING

Allow quick driver reports.

Categories:

- speed camera
- signal camera
- combined camera
- police/enforcement
- no entry
- restricted turn
- closure
- road work
- incorrect speed limit
- incorrect map data
- parking restriction
- hazard

Reporting UI must require minimal interaction.

While vehicle movement indicates driving, obey platform driver-distraction rules.

---

# 43. COMMUNITY VERIFICATION

Other drivers may confirm:

- Still there
- Not there
- Incorrect
- Updated

Do not immediately promote a single report to verified production data.

Use:

- number of independent reporters
- trust score
- time
- proximity
- contradictory reports
- official/licensed source matches
- historical consistency

Generate confidence.

---

# 44. SOURCE CONFIDENCE

Create explicit source classes.

Conceptual hierarchy:

```text
OFFICIAL_AUTHORITY
LICENSED_PROVIDER
FIELD_VERIFIED
MULTI_SOURCE_CONFIRMED
OSM
MULTIPLE_COMMUNITY_REPORTS
SINGLE_COMMUNITY_REPORT
UNKNOWN
```

Exact confidence formula should be configurable and tested.

Never present a single anonymous user report as official fact.

---

# 45. CHALLAN INTELLIGENCE

Provide optional challan upload.

The user may upload:

- screenshot
- image
- PDF

Extract only data relevant to analytics:

- offence type
- general violation location
- date/time
- amount
- relevant road/junction
- enforcement category

Redact/delete unnecessary personal information.

Do not retain:

- owner name
- address
- registration number
- personally identifying information

unless explicitly necessary and consented to.

Make privacy minimization the default.

---

# 46. CHALLAN HOTSPOTS

Aggregate sufficiently anonymized challan events.

Create map layer:

## Challan Hotspots

Do not claim every hotspot represents a camera.

Classify by:

- overspeed
- signal violation
- prohibited turn
- no entry
- parking
- other

Display statistical confidence/sample size.

Avoid exposing individual users.

---

# 47. TRIP REPORT

After journey:

Example:

```text
DriveGuard Trip Report

26.7 km
57 minutes

2 speed alerts
1 restricted-turn warning
3 enforcement points passed

0 detected probable compliance issues
```

Optionally:

“Potential fines avoided” may be shown ONLY as explicitly labelled estimates based on current published fine schedules, never guaranteed savings.

---

# 48. TRIP HISTORY

Users may opt to store:

- origin/general location
- destination
- route summary
- duration
- distance
- compliance event counts

Make full GPS trace storage optional.

Default to privacy minimization.

---

# 49. OFFLINE SUPPORT

Build an offline compliance cache.

Allow:

**Download Mumbai Compliance Pack**

Store locally:

- camera records
- restrictions
- signal locations
- speed-limit information where licensing permits
- critical junction geometry
- latest temporary restrictions
- road-compliance metadata

Respect provider storage terms.

Do not cache proprietary provider data when contract disallows it.

When offline:

- compliance alerts should continue from legally cacheable data
- navigation behavior depends on provider capability
- clearly indicate data freshness

---

# 50. DATA FRESHNESS

Every dynamic rule should expose:

- last updated
- effective time
- source freshness
- expiry
- last verification

Temporary orders should automatically deactivate after verified expiry.

“Until further order” should remain active but trigger periodic revalidation.

---

# 51. ADMIN DASHBOARD

Build a full web admin application.

Use it for:

- map data review
- camera verification
- signal verification
- restriction verification
- official notice review
- user report moderation
- duplicate merging
- geometry correction
- confidence override
- source comparison
- expiry handling
- audit history

---

# 52. ADMIN ENFORCEMENT MAP

Admin needs a full-screen geospatial interface.

Filters:

- camera type
- confidence
- status
- source
- last verified
- stale
- disputed
- user reported
- official
- licensed
- road segment
- Mumbai traffic division

Click record → edit/review.

---

# 53. ADMIN DATA COVERAGE DASHBOARD

Show REAL measured metrics.

Example structure:

```text
Mumbai Data Coverage

Road network coverage
Known speed-limit coverage
Traffic-signal coverage
Turn-restriction coverage

Speed cameras
  verified
  probable
  needs review

Red-light cameras
  verified
  probable
  needs review

Temporary orders
  last sync
  unprocessed
  review queue

Critical junctions
  fully verified
  uncertain
```

Never populate fake percentages.

Calculate from actual database coverage.

---

# 54. DATA REVIEW QUEUE

Every uncertain item enters:

`review_queue`

Reasons:

- uncertain geocoding
- multiple roads with same name
- conflicting sources
- direction unknown
- enforcement type uncertain
- speed limit conflict
- duplicate candidate
- expired source
- user dispute

Admin can:

- approve
- reject
- merge
- edit
- defer
- request field verification

---

# 55. AUDIT LOG

Every production compliance-data change must record:

- who/what changed it
- timestamp
- previous value
- new value
- source
- reason

Never silently rewrite enforcement data.

---

# 56. OPTIONAL FIELD-VERIFICATION WORKFLOW

Create admin functionality to generate verification tasks:

Example:

```text
Verify camera candidate:
Western Express Highway
Direction unknown
Source confidence 0.62
```

Allow verified team members to submit:

- coordinates
- direction
- photograph
- road/carriageway
- camera type

Do not require this to operate the initial application but implement the workflow.

---

# 57. DASHCAM / TRAFFIC-SIGN AI

Build this as an optional feature behind a feature flag.

Architecture:

```text
camera frame
 ↓
on-device CV
 ↓
traffic-sign candidate
 ↓
temporal confirmation
 ↓
geo-tag
 ↓
compare with database
 ↓
candidate correction
```

Target detection:

- speed-limit signs
- no entry
- no left
- no right
- no U-turn
- relevant parking signs

Do not send continuous camera footage to servers by default.

Prefer on-device inference.

Do not overwrite map data automatically.

Detected discrepancies enter review.

If a suitable properly licensed production model cannot be sourced, implement the complete interface/pipeline/feature flag and document the model dependency rather than fabricating a model.

---

# 58. AUTOMATIC DATA LEARNING

Example:

Database speed limit = 60.

Multiple high-confidence sign observations indicate 40.

Create:

```text
Candidate speed-limit update
DB: 60
Observed: 40
Confidence: ...
Evidence count: ...
```

Require validation before publication.

---

# 59. TECH STACK

Unless current official SDK compatibility strongly requires a change, use:

## Mobile
Flutter, latest stable production release.

Dart.

Use clean feature-oriented architecture.

## Android native
Kotlin.

Use native Android components where Flutter is insufficient for:

- navigation SDK integration
- foreground location
- Android Auto
- platform audio
- background service
- OS-specific lifecycle

## iOS native
Swift.

Use:

- Core Location
- platform navigation integration
- CarPlay architecture
- native background navigation capabilities where permitted

## Backend
Python.

FastAPI.

Use async APIs where useful.

## Database
PostgreSQL + PostGIS.

PostGIS is mandatory.

## Cache
Redis.

## Jobs
Choose a robust Python job queue appropriate to the stack.

Examples:
- Celery
- Dramatiq
- RQ

Document decision.

## Admin
Next.js + TypeScript.

## Auth
Use a production-ready provider or self-managed standard solution.

Examples:
- Supabase Auth
- Firebase Auth
- Auth0

Choose one and abstract critical dependencies.

Guest navigation must work without forcing account creation.

## Storage
S3-compatible object storage.

## Push
FCM / APNs.

## Error tracking
Sentry.

## Product analytics
PostHog or equivalent.

Privacy controls must be implemented.

## Infrastructure
Docker.

Terraform for production infrastructure.

GitHub Actions CI/CD.

---

# 60. MONOREPO STRUCTURE

Create approximately:

```text
driveguard/
│
├── apps/
│   ├── mobile/
│   ├── admin/
│   └── web/
│
├── native/
│   ├── android/
│   └── ios/
│
├── backend/
│   ├── api/
│   ├── workers/
│   ├── ingestion/
│   ├── compliance/
│   ├── geospatial/
│   ├── routing/
│   ├── moderation/
│   └── ai/
│
├── packages/
│   ├── domain-models/
│   ├── compliance-engine/
│   ├── alert-engine/
│   ├── provider-contracts/
│   ├── simulation/
│   └── shared-schemas/
│
├── data/
│   ├── seed/
│   ├── fixtures/
│   ├── osm/
│   └── synthetic/
│
├── tests/
│   ├── unit/
│   ├── integration/
│   ├── provider-contract/
│   ├── simulation/
│   ├── golden-routes/
│   ├── mobile/
│   └── e2e/
│
├── infrastructure/
│
├── scripts/
│
├── docs/
│
├── .github/
│   └── workflows/
│
├── docker-compose.yml
└── README.md
```

Improve where necessary, but maintain clean boundaries.

---

# 61. DATABASE SCHEMA

Design normalized production schemas for at least:

```text
users
user_preferences
vehicles

favorites
recent_places

navigation_sessions
trips
trip_events

road_segments
road_segment_levels
speed_limits

traffic_signal_junctions
signal_approaches
signal_stop_lines
signal_movements

turn_restrictions
access_restrictions
temporary_restrictions

enforcement_points
enforcement_zones
enforcement_observations

data_sources
source_documents
source_document_versions

ingestion_jobs
ingestion_runs

community_reports
report_confirmations
reporter_reputation

challan_uploads
challan_events

route_compliance_scans
route_compliance_events

review_queue
admin_decisions
audit_log

offline_pack_versions
```

Use PostGIS indexes.

Use appropriate:
- GiST/SP-GiST indexes
- B-tree indexes
- temporal indexes

Test geographic query performance.

---

# 62. DATA SOURCE SCHEMA

Each source must include:

```text
id
name
type
authority_level
license
usage_constraints
cache_allowed
redistribution_allowed
attribution_requirements
base_confidence
last_checked
status
```

This allows legal/data provenance to be programmatically enforced.

---

# 63. API

Create a documented REST API or carefully justified alternative.

Endpoints should cover:

- authentication
- user preferences
- vehicles
- favorites
- enforcement tiles/query
- nearby enforcement
- route compliance scan
- compliance events
- temporary restrictions
- traffic signals
- community reporting
- confirmations
- challan upload
- trip report
- offline pack metadata
- admin review
- data coverage
- ingestion status

Generate OpenAPI documentation automatically.

---

# 64. GEOSPATIAL QUERIES

Implement efficient operations such as:

- enforcement points within corridor
- restrictions along route
- relevant cameras ahead
- current road candidate search
- junctions ahead
- nearest speed-limit segment
- road-level filtering
- direction matching
- route intersection with active restrictions

Avoid repeatedly scanning the full dataset.

---

# 65. ROUTE CORRIDOR

When route is generated:

create a narrow route corridor.

Query DriveGuard data intersecting the corridor.

Then project each event onto route polyline.

Calculate:

- along-route distance
- order
- direction relevance
- entry/exit
- active state

Cache the route compliance plan locally.

---

# 66. LIVE COMPLIANCE PIPELINE

During navigation:

```text
Location sample
    ↓
Location filter
    ↓
Map matcher
    ↓
Matched road state
    ↓
Route progress
    ↓
Upcoming compliance index
    ↓
Rule evaluator
    ↓
Alert arbitration
    ↓
Visual / Voice / Haptic
```

Target low latency.

Avoid server dependency for every GPS sample.

---

# 67. LOCAL-FIRST LIVE ENGINE

Route-specific relevant events should be downloaded/cached at journey start.

The phone should be capable of determining most immediate alerts locally.

Benefits:

- lower latency
- less API cost
- works through temporary signal loss
- better privacy

Server remains authoritative for updates.

---

# 68. BACKGROUND LOCATION

Implement correctly according to CURRENT Android/iOS platform rules.

Do not hack around lifecycle restrictions.

Android:

Use the appropriate foreground navigation/location service and required notification/permissions.

iOS:

Use supported background location/navigation mechanisms.

Clearly explain permissions.

Only track location when required.

Stop tracking when drive ends.

---

# 69. BATTERY USAGE

Optimize:

- GPS update frequency
- map matching
- background work
- network refresh
- screen rendering

Adapt sampling to vehicle movement.

Do not run unnecessary high-frequency work when stationary.

---

# 70. ANDROID AUTO

Build proper Android Auto navigation support using current official Android for Cars navigation APIs/templates.

Show:

- turn guidance
- route
- ETA
- speed limit where allowed
- critical DriveGuard warnings where template/API permits
- safe report actions where permitted

Follow automotive distraction rules.

Do not attempt unsupported custom UI.

---

# 71. APPLE CARPLAY

Build the navigation integration architecture.

Research current CarPlay requirements.

If entitlement is unavailable during development:

- implement all code that can legally/technically be built
- create feature flag
- document exact entitlement step
- keep phone navigation fully operational

Do not claim CarPlay production support until entitlement/testing exists.

---

# 72. SEARCH EXPERIENCE

Search should be excellent.

Include:

- debounce
- current-location bias
- Mumbai geographic bias at initial launch
- typo tolerance where provider supports
- POI categories
- recents
- favorites
- landmark search

Search results should show useful locality context.

---

# 73. HOME / WORK

Allow:

- set Home
- set Work
- favorites

Store securely.

Guest user may store locally.

Authenticated user may sync.

---

# 74. TRAFFIC

Use live traffic where chosen provider allows.

Display:

- congestion on route
- ETA adjustment
- rerouting when worthwhile
- road closure data

DriveGuard temporary restrictions should additionally influence routing.

---

# 75. REROUTING

Trigger rerouting for:

- missed turn
- closure
- verified new restriction
- significantly faster route
- navigation deviation
- prohibited maneuver discovered

Do not constantly reroute for tiny ETA differences.

---

# 76. REPORT BUTTON

During drive, a single report control can open a minimal safe reporting interface.

Use large touch targets.

Allow voice reporting later if appropriate.

Never require typing while driving.

---

# 77. OFF-ROUTE / GPS FAILURE

Handle:

- tunnels
- GPS drift
- urban canyon
- wrong-road snap
- stationary traffic
- flyovers
- parallel service roads

When confidence falls below threshold:

suppress high-confidence claims rather than issuing potentially false warnings.

---

# 78. LOCATION CONFIDENCE

Maintain:

```text
location confidence
map match confidence
road level confidence
direction confidence
```

Alert logic must require appropriate confidence.

---

# 79. ENFORCEMENT VERIFICATION STATES

Use clear states:

```text
VERIFIED
PROBABLE
REPORTED
DISPUTED
STALE
INACTIVE
REMOVED
```

Default driver alerts should prioritize VERIFIED/strong PROBABLE records.

Let users opt into reported records visually.

---

# 80. ENFORCEMENT ICON OPACITY

Map styling can communicate confidence.

Example:

verified → solid

probable → normal

reported → lighter/dashed indicator

Do not overcomplicate.

---

# 81. USER TRUST

Every data object should internally answer:

“Why do we believe this?”

Maintain provenance.

This is a trust product.

False alerts will destroy usage.

Optimize precision before alert quantity.

---

# 82. PRIVACY

Precise driving location is sensitive.

Implement privacy by design.

Requirements:

- TLS
- encrypted sensitive data at rest
- minimal collection
- guest mode
- delete account
- delete trip data
- configurable history
- no sale of precise driving traces
- explicit analytics consent where required
- redact challans
- secure upload URLs
- short retention for raw evidence where possible

---

# 83. SECURITY

Implement:

- secure token storage
- refresh-token handling
- rate limiting
- request validation
- SQL injection protection
- SSRF protections
- file upload validation
- MIME verification
- malware scanning path
- API authorization
- role-based admin access
- CSRF where applicable
- secrets management
- no API keys in mobile source
- backend proxy where provider terms require
- signed admin audit logs

Run static security tools.

---

# 84. ABUSE PREVENTION

Crowdsourcing needs:

- rate limits
- reputation
- duplicate detection
- suspicious coordinate detection
- spam moderation
- user blocking
- device/account abuse signals
- admin review

Do not let malicious users create fake speed cameras visible as verified.

---

# 85. OBSERVABILITY

Implement:

- structured logging
- crash reporting
- API metrics
- worker metrics
- ingestion success/failure
- map provider error rate
- navigation errors
- alert counts
- false-report feedback
- data freshness
- DB latency

Use OpenTelemetry where useful.

---

# 86. FEATURE FLAGS

Implement feature flags for:

- dashcam AI
- challan upload
- live signal countdowns
- community enforcement reports
- CarPlay
- Android Auto
- alternative map provider
- experimental route scoring

This allows safe rollout.

---

# 87. ANALYTICS

Track privacy-conscious product metrics:

- search → route conversion
- navigation starts
- completion
- reroutes
- camera warnings
- turn warnings
- false-warning reports
- report submissions
- crashes
- battery complaints
- route scan use

Never log raw precise traces unnecessarily into analytics platforms.

---

# 88. GPS REPLAY SIMULATOR

BUILD THIS FROM THE BEGINNING.

Create:

`GPSReplayEngine`

It must replay:

- GPX
- JSON traces
- synthetic traces

Control:

- time scale
- speed
- pause
- jump
- GPS noise
- dropout
- heading
- road selection

Feed samples through the exact production compliance engine.

---

# 89. GOLDEN ROUTE TEST SUITE

Create a golden Mumbai scenario test system.

Do not fabricate factual road laws in production.

For tests, use clearly synthetic/fixture scenarios and verified real scenarios where sourced.

Scenario categories:

- speed camera ahead
- camera opposite carriageway
- camera under flyover
- camera on service road
- red-light camera
- normal signal
- no-left turn
- no-right turn
- no-U-turn
- no-entry
- one-way
- timed restriction active
- timed restriction inactive
- temporary closure
- speed-limit transition
- GPS drift
- reroute
- offline
- stale camera
- disputed camera
- vehicle-specific restriction
- overlapping alerts

---

# 90. ALERT TEST ASSERTIONS

Example synthetic test:

```text
limit = 50
camera direction = southbound
vehicle southbound

distance = 700m
speed = 62
```

Expect:

- applicable camera selected
- speed alert state active
- camera voice alert once
- visual event shown

Opposite-direction version:

Expect:

- map marker may be visible
- no voice camera warning

---

# 91. FLYOVER TEST

Synthetic topology:

```text
Level +1: flyover
Level 0: surface road
camera on Level 0
vehicle Level +1
```

Assert:

NO camera alert.

This is mandatory.

---

# 92. PARALLEL ROAD TEST

Place camera on service road.

Vehicle on main carriageway.

Assert no false warning unless camera enforcement geometry actually applies.

---

# 93. RESTRICTED-TURN TEST

If route provider proposes a maneuver that DriveGuard verifies as prohibited:

Compliance layer must reject it and request/recompute valid route.

Write regression test.

---

# 94. TEMPORAL RESTRICTION TESTS

Test:

- weekdays
- weekends
- times
- start/end dates
- overnight spans
- expiry
- “until further order”
- vehicle classes

Use India timezone correctly.

---

# 95. UNIT TESTS

Achieve strong coverage in critical deterministic modules:

- compliance rules
- temporal logic
- direction math
- route projection
- map matching helpers
- confidence
- alert arbitration
- deduplication
- speed hysteresis

Do not chase superficial 100% coverage.

Focus on safety-critical logic.

---

# 96. INTEGRATION TESTS

Cover:

- DB + PostGIS
- API
- ingestion
- source versioning
- offline pack
- route scanner
- reports
- admin review
- confidence promotion

---

# 97. PROVIDER CONTRACT TESTS

Every provider adapter must satisfy a common contract.

A provider switch must not require app logic rewrite.

Mock paid provider APIs in CI.

Never run expensive paid API calls in every test.

---

# 98. MOBILE UI TESTS

Test:

- search
- route selection
- start navigation
- layers
- camera details
- warning overlay
- Copilot Mode
- permissions
- offline
- dark mode
- settings

Use golden/screenshot tests appropriately.

---

# 99. ACCESSIBILITY

Check:

- text scaling
- screen readers
- color contrast
- touch targets
- icon labels
- voice alternatives
- reduced motion

Never communicate critical warning solely by color.

---

# 100. DRIVER-DISTRACTION UX

When driving:

- reduce interaction complexity
- enlarge targets
- suppress setup screens
- prioritize voice
- avoid unnecessary animations
- do not expose complex admin/report forms

Detecting movement must not incorrectly lock out a passenger from necessary non-driving interactions where platforms allow reasonable handling, but remain safety-focused.

---

# 101. LOCAL DEVELOPMENT

One command should start backend dependencies.

Example:

```bash
docker compose up
```

Provide seed synthetic test data.

Provide scripts for:

- migrations
- development DB
- synthetic Mumbai-like test environment
- API
- workers
- admin

Do NOT ship synthetic data as production.

---

# 102. ENVIRONMENT VARIABLES

Provide:

`.env.example`

Include placeholders for:

- navigation provider credentials
- Mappls credentials
- Google credentials
- auth
- database
- Redis
- object storage
- analytics
- Sentry
- LLM provider
- push
- signing

Never commit secrets.

---

# 103. PRODUCTION INFRASTRUCTURE

Build Terraform for a sensible production environment.

Prefer reliable managed infrastructure.

Target architecture may use:

- managed PostgreSQL/PostGIS
- containerized FastAPI
- managed Redis
- S3-compatible storage
- CDN
- secrets manager
- job workers
- queue
- monitoring

Design to scale horizontally.

Do not prematurely create absurd microservices.

Start as a modular monolith with clearly isolated domain modules where possible.

---

# 104. PERFORMANCE

Target:

- smooth 60 FPS map/navigation UI on common Android devices
- alert evaluation in milliseconds locally
- fast nearby-enforcement queries
- route scan in reasonable interactive time
- no repeated heavy DB spatial scans
- efficient vector/geospatial payloads
- proper pagination
- caching

Profile rather than guess.

---

# 105. OFFLINE PACK FORMAT

Version offline packs.

Include:

```text
city
version
generated_at
valid_until
schema_version
data_source_versions
checksum
```

Support delta update eventually.

Validate checksum before install.

---

# 106. VERSIONED COMPLIANCE SCHEMA

Mobile and server must negotiate schema versions.

Never break old offline clients without graceful handling.

---

# 107. WEB LANDING PAGE

Build a simple polished marketing website.

Include:

- product explanation
- screenshots/placeholders generated from actual UI
- safety positioning
- features
- coverage status
- privacy
- download links when available
- contact
- terms
- data feedback form

No exaggerated claims.

---

# 108. LEGAL / ATTRIBUTION SCREEN

Provide:

- map provider attribution
- OSM attribution where applicable
- source acknowledgements
- data limitation disclaimer
- privacy policy
- terms
- open-source licenses

Follow current provider rules exactly.

---

# 109. APPLICATION SETTINGS

Include:

## Navigation
- route preferences
- tolls
- highways where provider supports

## Alerts
- speed warnings
- camera warnings
- signal enforcement
- restricted turns
- temporary restrictions
- voice/haptic

## Map
- traffic
- enforcement
- signals
- community reports
- challan hotspots

## Privacy
- trip history
- analytics
- challan data
- delete data

## Offline
- Mumbai Compliance Pack

## Vehicle
- current vehicle profile

---

# 110. NOTIFICATION POLICY

Outside active driving, only send useful notifications.

Examples:

- important restriction affecting saved commute
- offline pack significantly outdated
- previously reported data verified

Do not spam.

---

# 111. ROUTINE-ROUTE INTELLIGENCE

Architecture may support frequent-route awareness.

Example:

“New verified restriction on your usual route.”

Must be optional.

Do not create invasive constant location tracking.

---

# 112. DATA DOWNLOAD / PORTABILITY

Authenticated user can request/export their stored personal data.

Support deletion.

---

# 113. IMPLEMENTATION OF REAL CAMERA DATA

This is critical.

You must actively investigate legally usable sources for Mumbai enforcement locations.

Prioritize:

1. official government/public authority sources
2. licensed map/navigation providers
3. independently verifiable open datasets
4. OSM where relevant
5. verified field observations
6. multi-user community reports

Do not scrape a random website and silently make it production truth.

For every source:

- inspect terms
- determine storage rights
- determine attribution
- determine redistribution restrictions
- document it

---

# 114. CAMERA COVERAGE STATUS

The application/admin must distinguish:

```text
Known verified cameras
Probable cameras
Reported cameras
Coverage unknown
```

Do not claim:

“All Mumbai cameras”

unless a truly authoritative exhaustive dataset supports that claim.

The product goal is exhaustive coverage; the software must honestly measure what has actually been verified.

---

# 115. DATA CONTRADICTION HANDLING

Example:

Provider A:
camera = speed camera

Provider B:
camera = traffic CCTV

Community:
camera removed

Do NOT blindly select one.

Create contradiction record.

Calculate confidence.

Queue review if material.

---

# 116. SPEED-LIMIT CONTRADICTIONS

If:

OSM says 60
provider says 50
sign observations say 50

Resolve according to:
- authority
- recency
- field evidence
- source rights

Store all observations.

Production active value is versioned.

---

# 117. EVENT SOURCES

Source event metadata should include:

- source ID
- original record ID
- retrieval timestamp
- original URL/reference
- original document hash
- extractor version
- extraction model
- confidence

This makes data reproducible.

---

# 118. INGESTION SCHEDULING

Run appropriate jobs periodically for:

- official traffic notices
- provider updates where supported
- community report aging
- stale verification
- expired restrictions
- offline pack generation

Do not hammer public services.

Respect rate limits and robots/terms.

---

# 119. INGESTION FAILURE

If official ingestion stops:

admin dashboard must visibly warn:

```text
Mumbai Traffic Police sync failed
Last successful sync: ...
```

Never silently use stale data forever.

---

# 120. ADMIN ALERTS

Notify administrators about:

- ingestion failure
- large data contradiction
- sudden camera removals
- major road-order changes
- stale critical coverage
- queue backlog

---

# 121. SPEED CAMERA MAP BEFORE JOURNEY

The user must be able to open the application, pan around Mumbai, and visually see known verified camera locations even with no active route.

This is non-negotiable.

---

# 122. ROUTE CAMERA PREVIEW

Before starting:

Tap:

`6 speed cameras`

Then map highlights all six route-relevant cameras.

Allow user to inspect each.

---

# 123. CAMERA DISTANCE WHILE DRIVING

During navigation:

the next relevant camera must show countdown distance.

Example:

```text
📷 Speed camera
620 m
Limit 50
```

Update smoothly.

Do not announce every tiny distance change by voice.

---

# 124. SIGNAL DISTANCE

Same model:

```text
🚦 Signal
420 m
```

If enforcement verified:

```text
🚦📷 Signal enforcement
420 m
```

---

# 125. TRAFFIC-SIGNAL MOVEMENT RULES

At each sufficiently modeled junction:

DriveGuard should understand from each approach:

- straight allowed?
- left allowed?
- right allowed?
- U-turn allowed?
- conditional?
- lane restrictions?

Use these for route legality.

---

# 126. STOP-LINE MODEL

If stop-line geometry exists:

store it.

Use primarily for map context / future functionality.

Do not claim red-light violation detection solely from low-accuracy consumer GPS.

---

# 127. ROUTE PREVIEW

Provide step-by-step route preview.

Show:

- maneuvers
- enforcement
- speed transitions
- restrictions

Allow tapping event to jump map.

---

# 128. FAVORITE ROUTE / COMMUTE

Allow users to save common destinations rather than arbitrary GPS tracking.

Future commute monitoring should use opt-in.

---

# 129. ROUTE SHARING

Allow sharing destination/route link.

Do not expose private trip history accidentally.

---

# 130. APP STARTUP

Startup needs to be fast.

Do not show long splash animations.

Map should appear quickly.

---

# 131. FAILURE STATES

Design graceful UX for:

- no internet
- map provider down
- search unavailable
- GPS permission denied
- background permission denied
- provider quota exceeded
- compliance DB unavailable
- offline pack stale
- location inaccurate

Explain useful next action.

---

# 132. PROVIDER QUOTA PROTECTION

Implement:

- caching
- debouncing
- request coalescing
- server-side quota monitoring
- error backoff
- usage metrics

Avoid accidental expensive API explosions.

---

# 133. SECRET PROTECTION

Never expose unrestricted provider keys.

Apply Android/iOS package/bundle restrictions where supported.

Apply server-IP/domain restrictions.

Document credential setup.

---

# 134. BRANDING

Create a simple original DriveGuard design system.

Potential concept:

- shield/navigation symbol
- simple road/enforcement iconography
- modern neutral map overlay components

Do not overbrand the navigation interface.

Navigation utility comes first.

---

# 135. ICONOGRAPHY

Use consistent original/openly licensed icons.

Separate:

- camera
- red-light enforcement
- traffic signal
- restricted turn
- closure
- speed limit
- police/community report

Test readability at small map sizes.

---

# 136. COPY

Use concise Indian English.

Distance:

- metres below 1 km where appropriate
- kilometres above

Speed:

`km/h`

Currency:

`₹`

Time:
device locale.

---

# 137. INDIA-FIRST ROAD TERMINOLOGY

Handle terms such as:

- service road
- flyover
- underpass
- signal
- junction
- naka where useful as POI/search terminology
- Eastern/Western Express Highway
- link roads
- sea link
- toll plaza

Do not hard-code Mumbai-only assumptions into architecture.

---

# 138. MULTI-CITY MODEL

Database must support:

```text
country
state
metro_area
city
traffic_authority
traffic_division
```

Mumbai is initial content scope, not architectural limit.

---

# 139. DATA PACK GEOGRAPHY

Offline packs should eventually support:

- Mumbai
- Thane
- Navi Mumbai
- MMR
- Pune
- Maharashtra

Build generic region framework now.

---

# 140. APP STORE / PLAY STORE READINESS

Prepare:

- Android release configuration
- iOS release configuration
- permission descriptions
- privacy manifests where required
- store screenshots configuration
- app icons
- adaptive icons
- deep links
- crash symbol upload
- versioning
- release notes framework

Do not publish automatically without credentials/explicit approval.

---

# 141. DEEP LINKS

Support links to:

- destination
- route
- enforcement point
- report
- camera map location

Validate inputs.

---

# 142. CI/CD

GitHub Actions should run:

On PR:

- formatting
- lint
- type checking
- backend unit tests
- PostGIS integration tests
- Flutter tests
- admin tests
- provider contract mocks
- security checks

On main:

- build Docker images
- generate artifacts
- deploy staging where credentials exist

Production deployment should require protected/manual approval.

---

# 143. CODE QUALITY

Requirements:

- no giant god classes
- no duplicated compliance rules
- typed schemas
- clear interfaces
- migrations
- documentation
- consistent errors
- structured logs

Run static analysis.

---

# 144. NO FAKE IMPLEMENTATION

Do not “complete” features with code like:

```text
return true; // TODO
```

Do not create buttons that do nothing.

Do not mark features as complete if they only show mock data.

If external credentials/entitlements prevent live execution:

- fully implement adapter
- write contract tests/mocks
- expose feature as awaiting credentials
- document exact next action

---

# 145. EXTERNAL BLOCKERS

Do NOT stop the entire build because you do not have:

- paid API key
- CarPlay entitlement
- Apple signing certificate
- production domain
- official provider agreement

Continue building everything independent of those.

Use local/mock/dev adapters where required.

At the end, list blockers precisely.

---

# 146. BUILD WORKFLOW

Do NOT ask the user to manually micromanage the project.

Proceed autonomously.

### Step 1
Inspect repository.

### Step 2
Research current official documentation for all major dependencies/providers.

### Step 3
Create:
- architecture
- ADRs
- schema
- interface contracts
- build plan

### Step 4
Implement foundational monorepo/infrastructure.

### Step 5
Implement backend/domain/compliance.

### Step 6
Implement navigation provider adapters.

### Step 7
Implement mobile navigation UI.

### Step 8
Implement camera/signal map.

### Step 9
Implement live compliance/alerts.

### Step 10
Implement ingestion.

### Step 11
Implement admin.

### Step 12
Implement community/challan features.

### Step 13
Implement offline.

### Step 14
Implement Android Auto/CarPlay architecture.

### Step 15
Implement simulator/test harness.

### Step 16
Run complete test suite.

### Step 17
Fix failures.

### Step 18
Run static/security analysis.

### Step 19
Build release artifacts where possible.

### Step 20
Produce final implementation report.

Do not stop after planning.

---

# 147. ORCHESTRATION

If subagents are available, use them aggressively.

Suggested roles:

```text
Lead Orchestrator

├── Mobile / Flutter agent
├── Android native agent
├── iOS native agent
├── Navigation provider agent
├── Geospatial agent
├── Compliance engine agent
├── Backend/API agent
├── Data ingestion agent
├── Enforcement-data agent
├── Admin dashboard agent
├── AI extraction agent
├── Testing/simulation agent
├── Security agent
└── DevOps agent
```

The lead agent owns integration.

Subagents must not independently invent conflicting schemas.

Freeze shared contracts early.

---

# 148. PARALLEL DEVELOPMENT RULE

Parallelize independent modules.

But integrate continuously.

Do not wait until all agents finish before testing interfaces.

---

# 149. AGENT COMMUNICATION

Maintain:

`docs/architecture.md`

`docs/domain-model.md`

`docs/provider-contracts.md`

`docs/data-provenance.md`

`docs/provider-licensing.md`

`docs/testing.md`

These are the shared truth.

---

# 150. ARCHITECTURE DECISION RECORDS

Create ADRs for at least:

- Flutter vs alternatives
- production map/navigation provider
- compliance-data source isolation
- PostGIS schema
- map matching
- background navigation
- offline architecture
- auth
- infrastructure
- AI extraction
- community confidence scoring

---

# 151. README

README must allow a new engineer to:

- understand the product
- install dependencies
- configure env
- start backend
- start admin
- run mobile
- load synthetic test pack
- run simulation
- run tests
- understand provider keys
- understand what production data is currently available

---

# 152. DEVELOPER DEMO MODE

Add dev/demo mode.

Allow:

- simulated location
- synthetic cameras
- synthetic signals
- speed control
- route replay

Visually label:

`DEMO DATA`

Never confuse it with production.

---

# 153. IN-APP DEBUG PANEL

Development builds should expose:

- GPS coordinates
- GPS accuracy
- matched road ID
- map match confidence
- road level
- current rule
- next enforcement ID
- distance
- alert reason
- provider
- data version

This is invaluable for Mumbai field testing.

Never expose this by default in production.

---

# 154. FIELD-TEST LOGGING

Create optional diagnostic recording:

- anonymized route trace
- expected alert
- actual alert
- map match
- camera selection
- timestamps

Allow tester to mark:

- false positive
- missed alert
- wrong road
- wrong direction
- wrong speed limit

Upload only with explicit tester permission.

---

# 155. FALSE-POSITIVE FEEDBACK

Camera detail/warning should provide after journey:

`Was this correct?`

Responses:

- Yes
- Wrong road
- Wrong direction
- Camera not present
- Not enforcement
- Wrong speed limit

Feed review queue.

---

# 156. QUALITY BAR FOR MUMBAI LAUNCH

Do not consider Mumbai “production ready” solely because app builds.

Launch readiness requires measured:

- camera verification quality
- signal coverage
- turn-restriction accuracy
- speed-limit coverage
- official notice freshness
- map-match quality
- background reliability
- field-test results
- false-warning rate
- crash-free sessions
- battery usage

Build launch-readiness report generator.

---

# 157. KEY PRODUCT KPI

One important metric:

**Useful warnings / total warnings**

We want extremely low irrelevant-warning rate.

Trust is more important than alert quantity.

---

# 158. NO OVER-ALERTING

If multiple cameras are visible but irrelevant:

do not speak.

If a camera was just passed:

do not repeatedly alert.

If vehicle is stationary:

suppress unnecessary repeating warnings.

---

# 159. ROUTE ARRIVAL

When nearing destination:

de-emphasize enforcement cards unless safety-critical.

Provide normal navigation arrival experience.

---

# 160. PARKING INTELLIGENCE

Where authoritative data exists:

warn of destination no-parking restrictions.

Example:

> “No-parking restriction near destination.”

Do not claim parking availability without reliable data.

---

# 161. TEMPORARY EVENT TRAFFIC

Official temporary road restrictions must be considered in routing.

Examples include special events, processions, construction or police traffic arrangements.

If route intersects an active verified closure:

reroute.

---

# 162. TIME ZONE

India initial region:

`Asia/Kolkata`

Store timestamps in UTC.

Evaluate local road rules using correct local timezone.

---

# 163. MAP DATA VERSIONING

Store compliance data version with each navigation session.

This allows reproducing a reported bug later.

---

# 164. SESSION SNAPSHOT

At navigation start, store minimal diagnostic metadata:

- compliance pack version
- provider
- route hash
- app version

Avoid unnecessary personal retention.

---

# 165. ERROR REPORT REPRODUCTION

Given trip/session ID in testing/admin, allow replaying the compliance decisions against recorded diagnostic data where user/tester consent exists.

---

# 166. PRODUCTION DATABASE BACKUPS

Implement:

- scheduled backups
- restore documentation
- migration rollback strategy
- point-in-time recovery where infrastructure permits

---

# 167. DATA MIGRATIONS

Use Alembic or equivalent.

Never modify schema manually in production.

---

# 168. DEPENDENCY MANAGEMENT

Pin versions appropriately.

Use automated dependency update tooling.

Do not blindly upgrade navigation SDKs without tests.

---

# 169. PROVIDER RELEASE CHANGES

Create abstraction because navigation APIs change.

Test supported versions.

Document known provider limitations.

---

# 170. UI PERFORMANCE TESTING

Test map with:

- 10 markers
- 100
- 1,000 nearby candidates before clustering
- dense South Mumbai signal areas

Use clustering/spatial filtering.

---

# 171. SPATIAL PAYLOAD

Do not send entire Mumbai camera database on every API call.

Use:

- viewport queries
- route corridor
- tiles/geohash/H3 if justified
- offline region packs

Choose and document strategy.

---

# 172. H3 OPTIONAL

Consider H3 for:

- coverage statistics
- heatmaps
- reporting aggregation

Do not replace PostGIS road geometry with H3.

---

# 173. CHALLAN HEATMAP PRIVACY

Require enough aggregated observations before showing a hotspot.

Prevent inference about an individual.

---

# 174. MOBILE DATABASE

Use appropriate local storage.

For geospatial/offline objects consider SQLite with spatial-friendly indexing or another justified local structure.

Do not load everything into memory.

---

# 175. ROUTE EVENT INDEX

At navigation start build an ordered local list:

```text
RouteEvent {
  distanceFromStart
  eventType
  geometry
  applicability
  warningPolicy
}
```

Use binary/forward indexing as vehicle progresses.

---

# 176. CAMERA PASSED STATE

Once reliably passed:

mark route event passed.

Do not warn again unless reroute causes new approach.

---

# 177. U-TURN / BACKTRACK

If user turns around:

re-evaluate applicable route events and direction.

Do not permanently suppress a camera simply because it was passed in the opposite direction earlier.

---

# 178. SPEED GPS SMOOTHING

Use appropriate smoothing.

Avoid showing wild speed jumps caused by noisy GPS.

Do not excessively lag real speed.

---

# 179. LOCATION MOCK DETECTION

For development, allow mock locations.

For production analytics, optionally mark suspected mock locations.

Do not punish users based solely on uncertain detection.

---

# 180. NAVIGATION PROVIDER FALLBACK

If production provider temporarily fails during an active trip:

preserve as much cached route/compliance functionality as possible.

Do not crash.

---

# 181. MAP STYLE

Create original:

- standard day style
- navigation day style
- navigation night style

Emphasize:

- active route
- road geometry
- critical enforcement
- current vehicle

De-emphasize irrelevant POIs during active driving.

---

# 182. CAMERA MARKER COLLISION

Priority:

route-relevant verified camera > ordinary POI.

Prevent labels from overlapping maneuver UI.

---

# 183. SIGNAL CLUTTER

At low zoom:

cluster or hide ordinary traffic signals.

During navigation:

show signals relevant to route/approach.

---

# 184. ENFORCEMENT MAP LEGEND

Provide compact explanation.

Users should understand icon meaning.

---

# 185. ROUTE CAMERA COUNTS

Route scan should distinguish:

```text
Verified speed cameras: X
Verified signal enforcement: Y
Reported/unverified: Z
```

Do not combine them misleadingly.

---

# 186. USER CAMERA FILTER

Users may choose:

- verified only
- verified + probable
- all reports

Default to trusted information.

---

# 187. CAMERA ACTIVITY

If status unknown:

show:

`Status not recently verified`

rather than “active.”

---

# 188. SOURCE EXPOSURE

Do not expose confidential/licensed provider internals.

User-facing camera details can say:

- Official
- Licensed map data
- Community verified
- Multiple sources

without leaking prohibited raw source data.

Admin retains detailed provenance where licensing allows.

---

# 189. MONETIZATION ARCHITECTURE

Do not hard-lock features now, but structure for future:

Free:
- navigation
- essential safety/compliance
- basic camera/restriction warnings

Potential Pro:
- advanced route analytics
- advanced history
- family vehicles
- enhanced offline
- advanced commute intelligence

Never put essential safety warnings behind a paywall by default.

---

# 190. FLEET FUTURE

Design APIs so future B2B can support:

- fleets
- taxi operators
- logistics
- rentals
- corporate vehicles
- driving schools

Possible fleet dashboard later:

- aggregate compliance
- recurring hotspots
- route restrictions
- driver training

Do not bloat initial consumer UI with fleet features.

---

# 191. DATA API FUTURE

Treat the internal compliance graph as a potentially valuable independent platform.

Maintain clean domain boundaries.

Potential future product:

`DriveGuard Road Compliance API`

No need to commercially expose it now.

---

# 192. FUTURE INDIA EXPANSION

No hard-coded assumptions that every authority is Mumbai Traffic Police.

Implement generic:

`AuthorityAdapter`

Future:

- Maharashtra Highway Police
- Pune Traffic Police
- Bengaluru
- Delhi
- etc.

---

# 193. BUILD COMPLETENESS

The build is not finished until the repository contains:

- mobile app
- Android integration
- iOS integration
- backend
- database
- migrations
- compliance engine
- provider abstractions
- working navigation integration when credentials exist
- camera map
- enforcement alerts
- traffic signals
- restrictions
- route scanner
- Copilot Mode
- government-notice ingestion
- community reporting
- challan intelligence
- admin dashboard
- offline compliance packs
- simulator
- comprehensive tests
- CI
- infrastructure
- documentation
- production configuration
- release configuration

---

# 194. ACCEPTANCE TEST — FIRST-TIME USER

A new user installs DriveGuard.

They grant location permission.

Within seconds they see the map.

They tap:

`Where to?`

Search:

`Marine Drive`

Select result.

See multiple routes.

See:

- ETA
- distance
- camera count
- signal-enforcement count
- relevant restrictions

Tap Start.

Navigation begins.

No tutorial is required to understand basic operation.

PASS.

---

# 195. ACCEPTANCE TEST — CAMERA MAP

User opens Mumbai map.

Enforcement layer enabled.

Verified known cameras are geographically visible.

User taps one.

Correct source-backed details appear.

PASS.

---

# 196. ACCEPTANCE TEST — CAMERA WARNING

User approaches a verified applicable speed camera.

Map marker appears ahead.

Countdown distance decreases.

Voice announces camera at appropriate distance.

Speed limit is visible.

Opposite-direction camera does not trigger.

PASS.

---

# 197. ACCEPTANCE TEST — SPEEDING

User is on verified 50 km/h road.

Current smoothed speed exceeds configured threshold for sufficient duration.

UI warns.

Voice/haptic occurs according to policy.

Noise spike does not cause false alert.

PASS.

---

# 198. ACCEPTANCE TEST — WRONG LEFT

An active verified no-left restriction exists.

Routing cannot generate that left.

In Copilot Mode, approaching the illegal movement produces clear warning.

PASS.

---

# 199. ACCEPTANCE TEST — FLYOVER

Camera lies on surface road.

Vehicle drives flyover above.

No camera audio warning.

PASS.

---

# 200. ACCEPTANCE TEST — SIGNAL CAMERA

Verified red-light enforcement at upcoming signal.

Correct marker visible.

Relevant approach receives signal-enforcement notification.

Opposite/unrelated approach does not.

PASS.

---

# 201. ACCEPTANCE TEST — TEMPORARY ORDER

Official verified temporary road closure becomes active.

Route scanner detects it.

Navigation routes around it.

After expiry, restriction automatically stops applying according to source.

PASS.

---

# 202. ACCEPTANCE TEST — OFFLINE

User downloads current Mumbai Compliance Pack.

Network disappears.

Existing navigation route/compliance system continues as far as provider/offline capabilities permit.

Camera/restriction alerts from locally permitted cache continue.

PASS.

---

# 203. ACCEPTANCE TEST — DATA HONESTY

Coverage is incomplete.

Admin dashboard says so.

App does NOT fabricate missing cameras or claim complete Mumbai coverage.

PASS.

---

# 204. ACCEPTANCE TEST — UX

During normal navigation the screen contains only information useful to driving.

No giant admin-like dashboard.

No excessive camera clutter.

No simultaneous competing alerts.

PASS.

---

# 205. FINAL TESTING LOOP

After first complete implementation:

1. run formatters
2. run linters
3. run type checkers
4. run unit tests
5. run integration tests
6. run PostGIS tests
7. run provider contract tests
8. run Flutter tests
9. run web/admin tests
10. run simulator scenarios
11. run golden-route suite
12. run security scans
13. build Android
14. build iOS where environment permits
15. build admin/web
16. build Docker images
17. fix every blocker possible
18. rerun

Do not stop at the first test failure.

---

# 206. QUALITY ASSURANCE REPORT

Generate:

`docs/QA_REPORT.md`

Include:

- tests run
- pass/fail
- coverage
- unresolved issues
- provider limitations
- OS limitations
- data limitations
- camera coverage status
- restriction coverage status
- performance results
- build results

---

# 207. DATA COVERAGE REPORT

Generate:

`docs/MUMBAI_DATA_COVERAGE.md`

With ACTUAL values.

Include:

- sources evaluated
- licensing status
- number of verified enforcement points
- number probable
- number reported
- signal coverage
- turn restrictions
- speed limits
- temporary traffic-order ingestion
- known gaps

Never invent counts.

---

# 208. PROVIDER REPORT

Generate:

`docs/NAVIGATION_PROVIDER_DECISION.md`

Compare the actually evaluated providers.

Include:

- capabilities
- limitations
- current SDK support
- licensing
- cost implications
- camera/signal data availability
- offline
- Android/iOS
- automotive
- chosen default
- fallback

---

# 209. SECURITY REPORT

Generate:

`docs/SECURITY.md`

Include:

- threat model
- precise-location privacy
- authentication
- reporting abuse
- file uploads
- API security
- secret handling
- admin RBAC

---

# 210. DEPLOYMENT GUIDE

Generate:

`docs/DEPLOYMENT.md`

Include:

- backend
- database
- Redis
- storage
- domains
- secrets
- Android
- iOS
- admin
- CI/CD
- rollback
- backups

---

# 211. FIELD TEST GUIDE

Generate:

`docs/MUMBAI_FIELD_TESTING.md`

Describe safe testing methodology.

Testers must NEVER intentionally violate road rules to test alerts.

Validate using:

- legal drives
- passenger observation
- simulator
- map/source verification

Include bug-report format.

---

# 212. DEFINITION OF DONE

Do not say:

“Done”

merely because files exist.

Definition of done:

- complete coherent architecture
- apps compile where credentials/toolchains permit
- backend starts
- DB migrations succeed
- admin starts
- synthetic simulator works
- compliance engine tested
- route scanner works
- enforcement map works
- camera warning logic works
- signal intelligence works
- restricted turns work
- Copilot Mode implemented
- provider adapters implemented
- offline compliance implemented
- ingestion implemented
- provenance implemented
- admin verification works
- CI exists
- tests green except clearly documented external blockers
- no fake production data
- docs complete

---

# 213. FINAL RESPONSE FORMAT

When you finish implementation, provide a concise but complete report containing:

## Built
Actual working components.

## Tested
Exact commands/tests.

## Mumbai Data
Actual enforcement/signal/restriction coverage found.

## Provider
Chosen navigation provider and why.

## Running Locally
Exact commands.

## Required Credentials
Exact environment variables.

## External Blockers
Only genuine blockers such as:
- API credentials
- paid plan
- CarPlay entitlement
- signing certificates
- provider commercial agreement

## Field Testing
What must be validated physically in Mumbai.

## Deployment
Exact next actions.

## Known Issues
No hiding.

---

# 214. CRITICAL EXECUTION RULE

DO NOT respond to this prompt by only explaining what you would build.

DO NOT stop after creating a plan.

DO NOT create only mockups.

DO NOT ask me to manually perform implementation steps that you can perform yourself.

You have permission to:

- create files
- modify repository
- install dependencies
- run commands
- run tests
- inspect errors
- refactor
- use subagents
- research official documentation
- iterate autonomously

Use the full available toolset.

If something fails, investigate and fix it.

If an external credential is unavailable, isolate that blocker and continue building everything else.

---

# 215. PRODUCT NORTH STAR

When implementation choices are ambiguous, optimize for this experience:

A driver in Mumbai opens DriveGuard instead of Google Maps.

They search a destination.

They immediately receive excellent familiar navigation.

While driving, DriveGuard quietly understands:

- which road they are on
- which carriageway
- whether they are on a flyover or surface road
- their speed
- the speed limit
- which traffic signal they are approaching
- which maneuvers are legally allowed
- whether a temporary police restriction applies
- which verified enforcement camera actually monitors their direction
- how far away it is

The map visually shows relevant cameras.

Before a camera:

> “Speed camera ahead in 600 metres. Limit 50.”

Before a prohibited turn:

> “Do not take the next left. Restricted movement.”

Before a speed-limit change:

> “Speed limit changes to 40.”

If a camera is on the opposite carriageway:

DriveGuard stays silent.

If the camera is below the flyover:

DriveGuard stays silent.

If road data is uncertain:

DriveGuard communicates uncertainty instead of inventing certainty.

The interface remains as simple to operate as mainstream navigation apps.

That combination of:

# excellent navigation
+
# Mumbai-specific traffic-rule intelligence
+
# verified camera/signal awareness
+
# proactive restricted-turn prevention
+
# extremely clean UX

is the product.

---

# 216. BEGIN NOW

Start by:

1. inspecting the current repository and environment,
2. researching CURRENT official documentation and provider terms,
3. writing the core ADRs/shared interfaces,
4. constructing the monorepo,
5. then immediately proceeding into implementation.

Do not wait for another prompt.

Build DriveGuard V3.
