# DRIVEGUARD V3 — REAL-WORLD DATA, MUMBAI CAMERA, SIGNAL & ROAD-RULE INTELLIGENCE MANDATE

This prompt supplements the main DriveGuard V3 build prompt and UI/UX prompt.

The application is only valuable if its real-world traffic-rule and enforcement information is trustworthy.

Treat this entire section as NON-NEGOTIABLE.

# 1. PRIMARY DATA OBJECTIVE

Build the best legally obtainable, continuously maintainable Mumbai road-compliance dataset possible.

The system should attempt to know and map:

- fixed speed cameras
- red-light cameras
- combined red-light + speed enforcement cameras
- average-speed enforcement zones where applicable
- verified automated challan-enforcement locations
- traffic signals
- signal-controlled intersections
- speed limits
- speed-limit transitions
- no-left turns
- no-right turns
- no-U-turns
- no-entry roads
- one-way restrictions
- conditional restrictions
- vehicle restrictions
- temporary police traffic orders
- road closures
- diversions
- parking restrictions
- enforcement/challan hotspots
- road levels
- flyovers
- underpasses
- service roads
- carriageways
- monitored directions

The end goal is that DriveGuard can confidently tell the driver:

“Speed camera in 600 metres. Limit 50.”

and correctly determine whether that camera actually applies to their road, carriageway and direction.

# 2. NEVER INVENT PRODUCTION DATA

Under absolutely no circumstances create fake real-world camera coordinates, signal coordinates, speed limits or road restrictions merely to make the application look populated.

Production records require provenance.

Synthetic data is permitted ONLY for:

- development
- automated tests
- simulator
- screenshots explicitly marked as demo

Every synthetic record must contain:

`synthetic = true`

Production code must make it impossible to accidentally mix synthetic records with live records.

# 3. SOURCE DISCOVERY

Research CURRENT legitimate sources.

Prioritize:

1. official Mumbai Traffic Police
2. Maharashtra traffic/police authorities
3. BMC/MCGM traffic-related notices
4. government open-data portals
5. licensed navigation/map providers
6. OpenStreetMap where permitted
7. field verification
8. verified multi-user reports
9. challan-derived aggregate evidence

For every source determine:

- what data exists
- update frequency
- whether there is an API
- whether scraping is permitted
- storage rights
- caching rights
- redistribution rights
- attribution requirements
- commercial-use restrictions
- whether it can legally be combined with the chosen map provider

Document findings.

# 4. SOURCE REGISTRY

Create a production source registry.

Each source record should contain conceptually:

```text
id
name
authority
source_type
source_url
license
terms_url
commercial_use_allowed
persistent_storage_allowed
redistribution_allowed
map_overlay_allowed
attribution_required
base_confidence
update_frequency
last_checked_at
status
notes
```

The application must never silently treat scraped third-party information as official.

# 5. CAMERA COVERAGE PROJECT

Treat Mumbai camera acquisition as its own engineering project.

Implement:

```text
Source Discovery
      ↓
Raw Candidate Records
      ↓
Normalize
      ↓
Geocode
      ↓
Road Match
      ↓
Deduplicate
      ↓
Direction Analysis
      ↓
Cross-Source Comparison
      ↓
Confidence Score
      ↓
Review Queue
      ↓
Verified Production Record
```

# 6. CAMERA ATTRIBUTES

A camera record should support:

```text
id
enforcement_type
geometry
latitude
longitude

road_segment_id
road_name

carriageway
road_level

monitored_direction
direction_tolerance

monitored_lanes

speed_limit_kph
speed_limit_confidence

fixed_or_mobile

active_status

verification_status

source_records[]

first_seen_at
last_seen_at
last_verified_at

confidence_score

user_confirmation_count
contradiction_count

synthetic
```

# 7. CAMERA TYPES

At minimum distinguish:

```text
FIXED_SPEED
RED_LIGHT
COMBINED_SPEED_RED_LIGHT
AVERAGE_SPEED_ENTRY
AVERAGE_SPEED_EXIT
TRAFFIC_MONITORING_ONLY
ANPR_UNKNOWN_PURPOSE
COMMUNITY_REPORTED
UNKNOWN
```

Never call ordinary surveillance CCTV a speed camera without evidence.

# 8. DIRECTIONAL ENFORCEMENT

Direction is mandatory wherever possible.

Do not alert a driver if:

- camera monitors opposite carriageway
- camera monitors different road
- camera is on service road
- camera is under flyover
- camera is above/below user on another road level
- camera points away from vehicle

Implement heading/direction tolerance.

# 9. ROAD LEVEL

Mumbai contains many:

- flyovers
- underpasses
- elevated roads
- parallel carriageways
- service roads

Model road level explicitly.

Example:

```text
surface = 0
flyover = +1
elevated corridor = +2
underpass = -1
```

Do not blindly rely on exact integer level if map provider represents levels differently; normalize provider data into internal concepts.

# 10. SIGNAL DATABASE

Build signal intelligence separately from camera intelligence.

Represent:

```text
junction
geometry
approaches
stop_lines
lanes
permitted_movements
restricted_movements
signal_heads
signal_enforcement
signal_phase_source
signal_countdown_source
confidence
```

# 11. SIGNAL ENFORCEMENT

Distinguish:

Traffic signal

versus:

Traffic signal with verified automated enforcement.

User-facing UI must not imply every signal has a challan camera.

# 12. LIVE SIGNAL DATA

Only display countdown/timing if current legitimate data exists.

Never infer traffic-light phase from historical averages and present it as live.

If unavailable:

do not show timer.

# 13. SPEED LIMIT DATABASE

Build speed limits from authoritative/licensed/open sources.

Support:

- road-specific
- direction-specific
- conditional
- vehicle-specific
- time-specific
- temporary
- unknown

Do NOT interpolate a nearby road's limit as certainty.

# 14. SPEED LIMIT OBSERVATIONS

Maintain observations separately from active truth.

Example:

```text
SpeedLimitObservation
source
value
geometry
observed_at
confidence
evidence
```

Then resolve an active production value.

This permits conflicting data without losing history.

# 15. OFFICIAL NOTICE PIPELINE

Continuously ingest relevant Mumbai traffic notices.

Detect:

- new notice
- updated notice
- superseding notice
- cancelled notice
- expired notice

Use document hashing/versioning.

# 16. AI EXTRACTION RULE

LLM may extract structured meaning from official notice text.

It must return strict schema.

LLM output is a CANDIDATE.

It cannot directly alter live legal road rules without deterministic validation.

# 17. LOCATION RESOLUTION

Official notices often describe:

“from X junction to Y junction”

instead of coordinates.

Implement location resolution using:

- road names
- landmarks
- intersections
- geocoder
- road graph

When ambiguous:

queue human review.

Never guess silently.

# 18. TEMPORAL RULE ENGINE

Support:

- date ranges
- daily time ranges
- weekday/weekend
- holidays where explicitly defined
- overnight ranges
- recurring periods
- vehicle class
- exceptions
- until-further-orders

Use Asia/Kolkata for evaluation.

Store timestamps UTC.

# 19. OSM

Where OSM is used:

respect ODbL.

Preserve attribution.

Keep derived-data licensing implications documented.

Never contaminate a proprietary-licensed database with incompatible data without legal review.

# 20. COMMUNITY CAMERA REPORTS

Community report must initially be:

`REPORTED`

not verified.

Promotion requires sufficient evidence.

Consider:

- independent reports
- reporter trust
- time
- GPS proximity
- directional consistency
- photographic evidence
- provider match
- official match
- contradictory reports

# 21. REPORTER TRUST

Build reputation behind the scenes.

Do not gamify camera reporting.

Protect against:

- duplicate accounts
- GPS spoofing
- mass fake reports
- report brigading

# 22. CAMERA REMOVAL

A camera disappearing should not instantly delete history.

Statuses:

```text
ACTIVE_VERIFIED
ACTIVE_PROBABLE
REPORTED
STALE
DISPUTED
INACTIVE
REMOVED
```

Keep history/version.

# 23. CAMERA MAP COVERAGE

The user must be able to browse all sufficiently trusted Mumbai enforcement points on the map.

The admin should be able to see everything, including uncertain candidates.

Consumer defaults:

- verified visible
- probable configurable
- unverified hidden unless enabled

# 24. CAMERA CLUSTERING

At low map zoom:

cluster.

At active navigation:

prioritize route-relevant cameras.

# 25. CAMERA APPROACH QUERY

Given:

```text
current_position
matched_segment
current_heading
route
speed
```

return:

```text
next_applicable_enforcement[]
```

sorted by along-route distance.

Do not use Euclidean distance alone.

# 26. ROAD DISTANCE

Calculate remaining distance using route/road geometry.

Example:

A camera can be 100 m straight-line but 700 m road distance.

Use 700 m.

# 27. CAMERA WARNING POLICY

Warning distance should adapt to:

- speed
- road class
- upcoming turn
- number of competing alerts
- GPS confidence

Do not hard-code one radius globally.

# 28. COVERAGE METRICS

Create actual measurable Mumbai coverage.

Possible metrics:

```text
road km with known speed limit / relevant road km

modeled major junctions / known major junctions

verified cameras

probable cameras

reported cameras

verified turn restrictions

temporary notices processed

temporary notices awaiting review
```

Do not fake 99% numbers.

# 29. DATA QUALITY SCORE

Create internal quality metrics:

- completeness
- freshness
- authority
- cross-source consistency
- geometric accuracy
- directional accuracy

Use these to determine whether a warning should be issued.

# 30. FIELD VERIFICATION

Create an internal field-verification workflow.

A trusted verifier may submit:

- GPS position
- road name
- direction
- lane/carriageway
- photo
- camera category
- notes

Require safe passenger/static verification.

Never instruct testers to break laws.

# 31. CHALLAN DATA

Where user voluntarily uploads challan:

extract potentially useful road-rule evidence.

Remove personal details.

Use aggregate evidence to identify:

- enforcement hotspots
- recurring prohibited movements
- signal enforcement locations

Do NOT automatically infer exact camera location from challan alone unless evidence supports it.

# 32. ADMIN DATA REVIEW

Admin must be able to view evidence for every candidate.

Show:

- map
- sources
- source snippets
- candidate type
- proposed location
- proposed direction
- conflicts
- confidence

Actions:

- approve
- edit
- reject
- merge
- mark stale
- request field check

# 33. DATA AUDIT

Every change must be auditable.

Maintain:

before
after
actor
reason
source
timestamp

# 34. PRODUCTION SAFEGUARD

No new candidate becomes a high-confidence driver warning merely because an AI model says so.

Use deterministic promotion rules plus authority/confidence.

# 35. LAUNCH GOAL

The goal is eventually excellent Mumbai coverage.

But app must state measured reality.

Never market:

“All Mumbai cameras”

until actual data supports that statement.

Instead internally target comprehensive coverage and expose accurate coverage status.

# 36. FINAL DATA DELIVERABLES

Create:

`docs/DATA_SOURCES.md`

`docs/DATA_LICENSING.md`

`docs/MUMBAI_CAMERA_COVERAGE.md`

`docs/MUMBAI_SIGNAL_COVERAGE.md`

`docs/MUMBAI_RESTRICTION_COVERAGE.md`

`docs/DATA_QUALITY_MODEL.md`

Include actual findings.

# 37. EXECUTION

Do not merely document this.

Implement:

- schemas
- pipelines
- APIs
- admin workflows
- confidence engine
- map rendering
- route queries
- ingestion workers
- tests

The quality of DriveGuard's Mumbai data is as important as the mobile application itself.

BEGIN.
