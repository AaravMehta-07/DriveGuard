# DRIVEGUARD V3 — ULTRA-DETAILED STEP-BY-STEP UI IMPLEMENTATION PROMPT
## Build the Consumer Navigation UI Methodically, Screen by Screen, State by State

This prompt supplements the DriveGuard V3 Master Build Prompt and Master UI/UX Design Prompt.

The purpose of this prompt is to remove ambiguity from UI implementation. Do not merely “make a clean UI.” Follow this implementation sequence and complete every screen, component, state, interaction, responsive layout, and visual review step.

You are implementing a consumer navigation product intended to feel immediately familiar to Google Maps users while remaining visually original, more compliance-aware, and uncluttered.

The desired outcome is:

**Mainstream navigation simplicity + premium polish + DriveGuard enforcement intelligence.**

Do not skip any section because another prompt already mentions it. This prompt is intentionally repetitive and operational so the implementation remains correct even if context becomes large.

---

# A. UI WORKING PRINCIPLES

1. The map is the primary canvas.
2. Search and navigation are the primary jobs.
3. Speed/camera/restriction intelligence must feel integrated, not bolted on.
4. A driver should understand critical information in under one second.
5. The active navigation screen must never resemble a dashboard.
6. Do not copy Google Maps pixel-for-pixel. Copy only broadly familiar interaction patterns.
7. Use original DriveGuard styling and iconography.
8. Prefer bottom sheets and contextual overlays instead of unnecessary full-screen pages.
9. One primary action per state.
10. One primary alert at a time.
11. Never use fake production data just to populate UI.
12. Synthetic/demo data must be clearly marked in development screenshots and tests.
13. Render and visually inspect the UI after implementation; compilation alone is not acceptance.

---

# B. BEFORE CODING SCREENS — CREATE THE DESIGN FOUNDATION

Complete these first.

## B1. Design tokens

Create centralized tokens for:

- brand accent
- background/surface colors
- day map overlay colors
- night map overlay colors
- primary text
- secondary text
- disabled text
- warning semantic color
- critical semantic color
- success/verified state
- probable/reported state
- route-selected state
- route-alternative state
- camera marker states
- signal marker states
- divider colors
- overlay scrims

Also define:

- spacing scale
- control heights
- icon sizes
- typography styles
- radii
- elevation levels
- animation durations
- animation curves
- map overlay z-order priorities

Do not scatter raw design constants through widgets.

## B2. Typography

Use a platform-appropriate modern sans-serif, preferably system fonts unless there is a compelling reason otherwise.

Create styles for:

- display navigation distance
- navigation action
- road name
- speed number
- speed-limit number
- ETA primary
- standard body
- secondary metadata
- tiny map annotation

Use medium/semibold weights where readability demands it. Avoid thin weights.

## B3. Icon system

Select one coherent general icon family, then create/customize original DriveGuard icons where needed.

You need consistent icons for:

- search
- microphone
- current location
- recenter
- map layers
- overview
- mute
- report
- Home
- Work
- favorite
- speed camera
- red-light enforcement
- combined enforcement
- average-speed zone
- ordinary traffic signal
- no-left
- no-right
- no-U-turn
- no-entry
- one-way
- road closure
- speed-limit change
- temporary restriction
- warning
- shield / DriveGuard
- offline
- privacy
- vehicle

Ensure every critical icon remains understandable in dark mode and at small map-marker sizes.

## B4. Consumer component library

Implement reusable widgets/components before building all screens:

- DriveGuardSearchBar
- PrimaryDriveButton
- MapFloatingControl
- MapLayerControl
- MapRecenterControl
- CurrentLocationMarker
- EnforcementMarker
- EnforcementClusterMarker
- TrafficSignalMarker
- RestrictionMarker
- DestinationMarker
- SelectedRouteOverlay
- AlternativeRouteOverlay
- NavigationManeuverCard
- SecondaryManeuverHint
- LaneGuidancePanel
- SpeedLimitBadge
- CurrentSpeedDisplay
- SpeedWarningState
- DriveGuardAlertCard
- CameraApproachCard
- RestrictionWarningCard
- SignalEnforcementCard
- RouteIntelligenceSummary
- RouteEventRow
- ETAFooter
- DestinationBottomSheet
- RouteSelectionBottomSheet
- CameraDetailBottomSheet
- LayersBottomSheet
- UpcomingEventsBottomSheet
- ReportBottomSheet
- CopilotActivePill
- PermissionExplanationSheet
- OfflineStatusBanner
- ErrorBanner
- Toast/InlineFeedback

Every reusable component must support:
- light mode
- dark mode
- disabled/loading states where relevant
- accessibility labels
- text scaling
- press/selected states
- narrow-screen behavior

---

# C. SCREEN 1 — APP LAUNCH / MAP HOME

Implement this first because it is the product entry point.

## C1. Initial load

Behavior:

1. Show lightweight branded splash only if technically needed for initialization.
2. Transition to map quickly.
3. Do not block with account creation.
4. If location permission has not been requested, show the map shell first and then a concise permission explanation.
5. Never present multiple permissions at once without context.

## C2. Home layout

Full-screen map.

Top safe-area:
- floating search bar
- optional compact profile/menu control

Map:
- user location
- road labels
- traffic if enabled
- verified camera markers depending on zoom
- signal enforcement depending on zoom
- clusters at lower zoom

Lower area:
- Home shortcut
- Work shortcut
- recent place shortcuts
- `Start DriveGuard` Copilot CTA

Do not place a permanent bottom navigation bar unless later usability testing proves it necessary.

## C3. Search bar dimensions/behavior

Must:
- span most usable width
- have comfortable 48–56dp-ish touch height
- respect safe areas
- include search icon
- show `Where to?`
- include microphone only if functional
- animate into search state smoothly
- maintain clear contrast over map in day/night themes

Do not use a transparent search bar that becomes unreadable over map detail.

## C4. Home camera markers

At city-level zoom:
- cluster cameras
- hide ordinary traffic lights
- do not show every restriction

At neighborhood zoom:
- reveal individual verified cameras
- allow signal enforcement
- selectively show no-entry/restricted-turn markers

At street zoom:
- show richer enforcement detail

Implement marker density rules, not arbitrary always-on rendering.

---

# D. SCREEN 2 — SEARCH

## D1. Entry transition

Tap search field.

Animate into focused search experience without abrupt jarring navigation.

Top:
- back control
- focused text field
- clear-text action when content exists
- microphone if supported

## D2. Default search content

Before user types:

1. Home
2. Work
3. Recent destinations
4. Saved/favorites

Keep list compact.

## D3. Live autocomplete

As user types:
- debounce correctly
- show provider suggestions quickly
- bias toward Mumbai/current location
- show place name prominently
- show locality/address secondarily
- include simple category icon

Do not expose provider-specific IDs.

## D4. Loading

If results take noticeable time:
- subtle inline progress
- optional skeleton rows

No full-screen blocking spinner.

## D5. Empty/error states

No results:
`No places found`

Provider unavailable:
`Search is temporarily unavailable.`

Offline:
show downloaded/recent places if available.

---

# E. SCREEN 3 — DESTINATION DETAILS

When destination selected:

1. Return focus to map.
2. Center destination appropriately.
3. Show destination pin.
4. Open compact-to-medium bottom sheet.

Bottom sheet hierarchy:

- place name
- locality/address
- estimated travel time if already available
- primary `Directions`
- secondary Save/Share
- optional POI actions only if provider legitimately supports them

Do not overwhelm with ratings/photos/reviews unless such features become product requirements.

DriveGuard is navigation-first.

---

# F. SCREEN 4 — ROUTE SELECTION

This must feel instantly familiar.

## F1. Map state

Show:
- origin
- destination
- selected route
- alternative routes
- traffic state where provider supports it
- relevant verified enforcement markers
- closures/restrictions affecting route

Selected route:
strongest line.

Alternatives:
muted.

## F2. Route bottom sheet

Collapsed/medium state should show:

- destination
- selected route label
- ETA
- travel time
- distance
- arrival time
- traffic summary
- toll indicator if reliable
- DriveGuard Route Intelligence
- Preview
- START

## F3. Route Intelligence compact view

Display a concise line/group:

- speed-camera count
- signal-enforcement count
- restricted movement count
- speed-limit change count
- active closures if any

Do not show 20 event rows by default.

## F4. Route Intelligence expanded

Tap it to expand.

Show events sorted by along-route distance.

Each row:
- icon
- distance from start/current location
- event title
- relevant limit/status
- tap to center map

## F5. Camera count interaction

If user taps `6 speed cameras`:
- visually highlight those six cameras on selected route
- fit/retain route context
- allow individual camera tap
- do not navigate to a separate unrelated page

## F6. Route switching

User can:
- tap an alternative route line
- tap alternative route option in sheet

Both update:
- ETA
- route intelligence
- camera count
- restrictions
- selected route styling

## F7. START CTA

Primary CTA:
`START`

High contrast, accent-colored, large touch target.

It must not compete with any other equally strong button.

---

# G. SCREEN 5 — ROUTE PREVIEW

Implement a route preview mode.

Show:
- overview map
- step list
- enforcement/restriction events interleaved or clearly accessible
- speed-limit transitions where known

Tap step:
center corresponding route segment.

Tap enforcement event:
center camera/restriction.

Back:
return to route selection without losing selection.

---

# H. SCREEN 6 — ACTIVE NAVIGATION
## THIS IS THE MOST IMPORTANT UI IN THE APP

Build this carefully and test every state.

## H1. Permanent structure

Top:
NavigationManeuverCard.

Center:
Map.

Lower-left or lower-map area:
SpeedLimitBadge + CurrentSpeedDisplay.

Context area:
ONE primary DriveGuardAlertCard.

Bottom:
ETAFooter.

Secondary floating controls:
- recenter
- overview
- mute
- report

Do not add unrelated controls.

## H2. Maneuver card

Display:

- maneuver arrow
- distance
- action
- target road

Example hierarchy:

`450 m`
`Turn left`
`Marine Drive`

Use large glanceable text.

If lane guidance available:
display lane panel temporarily beneath/adjacent to maneuver card.

## H3. Map behavior

Default:
heading-up navigation perspective.

Active route:
dominant.

Current location:
clear.

Camera marker:
visible but subordinate to route.

Other cameras:
lower emphasis.

POIs:
reduced during navigation.

## H4. Current speed + speed limit

Always visible when reliable data exists.

Speed limit:
road-sign-inspired badge.

Current speed:
large numerical value.

Unknown limit:
do not guess; show `--` / `Limit unavailable`.

## H5. Normal navigation state

Only show:
- maneuver
- map
- speed/limit
- ETA
- next relevant DriveGuard item

Nothing else.

## H6. Speed-warning state

If mild overspeed:
subtle semantic emphasis.

If sustained meaningful overspeed:
stronger speed display + concise `Reduce speed`.

If severe:
voice/haptic per policy.

Do not turn entire screen red.

Do not flash.

## H7. Camera approach state

When relevant camera enters warning range:
show compact card:

`Speed camera`
`620 m`
`Limit 50 km/h`

The marker should be visible ahead on map if viewport allows.

Distance updates smoothly.

Audio must match card.

## H8. Camera + overspeed state

If camera ahead AND user overspeeding:
camera card remains, but speed warning gets appropriate prominence.

Example:
`Reduce speed · Limit 50`
secondary:
`Speed camera · 520 m`

## H9. Opposite-direction camera

Marker may remain visible but should be subdued.

No card.
No voice.
No haptic.

## H10. Flyover/surface mismatch

Irrelevant camera should not become upcoming event.

Do not confuse user simply because coordinates are nearby.

## H11. Restricted-turn state

This overrides ordinary camera cards.

Show:

`DO NOT TAKE NEXT LEFT`
`Restricted movement`
`120 m`

Use strong icon/contrast.

Voice:
`Do not take the next left. Continue straight.`

Do not display technical legal wording.

## H12. No-entry state

High-priority:

`DO NOT ENTER`
`Restricted road ahead`

If route active, trigger compliant reroute.

## H13. Signal-enforcement state

Card:

`Signal enforcement`
`420 m`

Do not imply the signal is currently red/green unless live data exists.

## H14. Upcoming speed-limit change

Show subtle event:
`40 km/h in 300 m`

After crossing verified boundary:
current limit updates.

## H15. ETA footer

Stable footer containing:

- remaining time
- distance
- arrival time

Example:
`39 min · 17 km · 10:14 AM`

Use stable layout to avoid jitter as values update.

---

# I. ACTIVE NAVIGATION SECONDARY INTERACTIONS

## I1. Map pan

If user pans:
- stop auto-follow temporarily
- show Recenter control
- maintain guidance/audio

## I2. Route overview

Tap overview:
- zoom to route
- show `Resume`/`Recenter`
- keep navigation active

## I3. Mute

Provide direct access.

Support:
- full guidance
- alerts only
- muted

Do not bury in Settings.

## I4. Upcoming sheet

Swipe/tap contextual strip.

Expanded sheet:

- next camera
- next signal enforcement
- next restriction
- next speed-limit change
- closure etc.

Rows ordered by route distance.

Keep map visible.

## I5. End navigation

Use deliberate secondary action.

Avoid accidental termination.

Confirm only if necessary; don't create annoying modal complexity.

---

# J. SCREEN 7 — COPILOT MODE

Copilot is for users with no destination or users running another navigation app.

## J1. Entry

Home:
`Start DriveGuard`

Tap.

If permissions ready:
start immediately.

## J2. Layout

Map full-screen.

Small top/upper status:
`DriveGuard Active`

Show:
- current road
- current speed
- speed limit
- next relevant enforcement
- nearby restricted-entry warnings

No route line.

## J3. Camera card

Same visual language as navigation.

`Speed camera`
`850 m`
`Limit 50`

## J4. Restricted movement

If user trajectory indicates direct prohibited entry:
promote critical warning.

## J5. Background state

Android persistent notification should clearly state DriveGuard active, with only useful information.

Avoid changing notification every second.

---

# K. SCREEN 8 — ENFORCEMENT MAP / CAMERA EXPLORER

This is explicitly required because users must be able to see where known cameras are.

## K1. Entry

Accessible from:
- layers
- map menu
- route camera count

No more than two obvious actions from home.

## K2. Layout

Full-screen map.

Top:
search.

Floating:
filters/layers.

Show verified cameras geographically.

## K3. Filter sheet

Allow:
- All enforcement
- Speed
- Red-light
- Combined
- Average speed
- Verified
- Probable
- Reported
- Signals
- Restrictions

Default should prioritize verified records.

## K4. Camera detail sheet

Tap camera.

Sheet:
- type
- road
- direction in natural language
- speed limit if known
- status
- last verified
- source category
- route relevance if route active

Avoid raw lat/lng in consumer UI.

## K5. Marker selection

Selected marker:
slightly emphasized.

Map retains enough surrounding road context.

## K6. Clusters

At low zoom:
cluster.

Tap cluster:
zoom in.

Do not simply display hundreds of overlapping camera icons.

---

# L. SCREEN 9 — LAYERS

Use a bottom sheet.

Sections:

## Map
- Traffic
- Satellite (if provider supports it)

## DriveGuard
- Speed cameras
- Signal enforcement
- Traffic signals
- Restricted turns
- No-entry
- Temporary restrictions

## Optional
- Challan hotspots
- Parking
- Community reports
- Reported/unverified cameras

Keep settings readable.

Use standard switches/check rows.

---

# M. SCREEN 10 — REPORT FLOW

During drive:
single report control.

Open large-button sheet.

Categories:
- Camera
- Signal camera
- Restriction
- Closure
- Police/enforcement
- Wrong speed limit
- Map issue

Moving vehicle:
do not require typing.

After selection:
`Thanks — report received.`

Detailed follow-up can occur after drive.

---

# N. SCREEN 11 — TRIP COMPLETE

On arrival:

`You've arrived`

Then compact trip summary sheet:

- distance
- duration
- speed warnings
- restricted-turn warnings
- enforcement points passed

Optional `View details`.

Do not use competitive driving scores or speed gamification.

---

# O. SCREEN 12 — TRIP HISTORY

Simple list.

Each row:
- destination
- date/time
- duration
- distance

Trip detail:
- route overview
- compliance event summary

Privacy controls:
- delete trip
- clear history
- disable history

---

# P. SCREEN 13 — SAVED PLACES

Simple standard list.

Support:
- Home
- Work
- favorites
- rename
- delete

Avoid collection complexity unless needed later.

---

# Q. SCREEN 14 — OFFLINE DATA

Title:
`Offline`

Card:
`Mumbai Compliance Pack`

Show:
- cameras
- signals
- restrictions
- speed-limit data where permitted
- temporary restrictions
- pack size
- updated date
- download/update state

States:
- not downloaded
- downloading
- downloaded
- update available
- stale
- error

Never imply proprietary map data is offline if provider licensing does not permit it.

---

# R. SCREEN 15 — SETTINGS

Use native-feeling settings list.

Sections:

Navigation
DriveGuard Alerts
Map
Vehicle
Offline
Privacy
About

Rows should be straightforward.

Do not create dashboard cards.

---

# S. SCREEN 16 — PERMISSIONS

Build contextual permission explanation components.

Location:
explain why needed.

Background location:
ask only when enabling active navigation/Copilot behavior requiring it.

Notifications:
ask only when useful.

Do not front-load five permission dialogs.

---

# T. SCREEN 17 — ERROR / DEGRADED STATES

Implement visually polished states for:

- GPS unavailable
- location accuracy low
- no internet
- search provider unavailable
- route unavailable
- compliance data unavailable
- offline pack stale
- navigation provider quota/failure
- background permission missing

Always tell user what still works.

Example:
`Navigation is temporarily unavailable. DriveGuard alerts can still run from downloaded data.`

---

# U. DAY/NIGHT IMPLEMENTATION

Do not simply invert colors.

## Day
- light neutral surfaces
- readable road labels
- clear active route
- subtle camera markers
- moderate elevation overlays

## Night
- dark charcoal/navy surfaces
- no pure-white giant panels
- retain semantic warning contrast
- maintain visible camera/restriction icons
- dim nonessential POIs

Test in dark room conditions.

---

# V. MAP MARKER Z-ORDER

Define explicit priority.

Highest:
1. critical restriction affecting current approach
2. current vehicle
3. active route
4. route-relevant verified enforcement
5. destination
6. relevant signal
7. other verified cameras
8. reported cameras
9. ordinary POIs

Prevent marker collision.

---

# W. ALERT PRIORITY VISUAL RULES

Only one prominent card at a time.

Priority example:

1. imminent prohibited movement / no entry
2. severe overspeed
3. closure / major restriction
4. camera enforcement
5. speed-limit change
6. ordinary signal
7. community report

Secondary information can remain minimal.

---

# X. RESPONSIVE BREAKPOINT CHECKLIST

Test every primary screen at:

- ~320 logical px width
- ~360
- ~390
- ~430+
- portrait
- landscape
- large text
- Android gesture nav
- iPhone safe areas

Ensure:
- no clipped search bar
- no overlapping speed badge
- no ETA overflow
- no hidden buttons
- bottom sheets stay reachable
- map controls stay inside safe areas

---

# Y. ACCESSIBILITY CHECKLIST

Every icon-only button:
semantic label.

Every critical state:
icon + text + color, never color alone.

Touch targets:
large enough.

Text scaling:
must not break navigation hierarchy.

Screen readers:
camera/restriction cards should announce concise, useful text.

Reduced motion:
animations should respect settings.

---

# Z. VISUAL INSPECTION LOOP — MANDATORY

After implementing each major screen:

1. run app
2. render screen with realistic synthetic/demo state
3. capture screenshot
4. inspect visually
5. list issues
6. fix them
7. recapture

Do not batch all visual inspection at end.

For active navigation, create screenshot states for:

- normal
- camera ahead
- camera ahead + overspeed
- restricted left
- no-entry
- signal enforcement
- speed-limit change
- GPS low confidence
- offline

---

# AA. ANTI-UGLY-UI CHECKLIST

Reject and rework any screen containing:

- random gradients
- too many cards
- huge empty top/bottom gaps
- tiny unreadable metadata
- inconsistent corner radii
- inconsistent icon stroke weights
- camera icons obscuring road labels
- 4+ floating action buttons
- overlapping bottom sheets
- debug-looking chips
- generic placeholder map pins
- excessive shadows
- too many colors
- weak contrast
- oversized title bars
- navigation instruction that wraps badly
- speed/limit hidden behind alerts

---

# AB. GOOGLE-MAPS-FAMILIAR USER MENTAL MODEL

A user familiar with Google Maps should instinctively know:

- where to search
- how to pick a destination
- how to choose route
- where START is
- what the top turn instruction means
- where ETA is
- how to recenter
- how to mute
- how to exit navigation

Do not innovate on these basics merely to appear original.

Innovation belongs in:

- route intelligence
- camera visibility
- speed-limit clarity
- enforcement distance
- restricted-turn warnings
- compliance confidence
- Copilot Mode

---

# AC. POLISH DETAILS

Implement subtle quality touches:

- map padding adjusts when sheets expand
- selected marker remains visible above sheet
- keyboard doesn't cover search results
- route overview accounts for bottom sheet height
- camera card transition does not jump map viewport
- ETA text does not reflow on every minute change
- marker clusters animate/transition modestly
- dark mode switches all overlays consistently
- device rotation preserves current navigation state
- bottom sheet drag handles are consistent
- toasts never cover ETA/speed
- current location marker has clear heading
- loading indicators are local, not full-screen when avoidable

---

# AD. UI TEST ARTIFACTS

Create:
- `docs/UI_UX_SPEC.md`
- `docs/SCREEN_INVENTORY.md`
- `docs/UI_STATE_MATRIX.md`
- `docs/MAP_MARKER_RULES.md`
- `docs/ALERT_VISUAL_PRIORITY.md`

Create golden/screenshot tests for all critical states.

---

# AE. IMPLEMENTATION ORDER

Use this exact high-level order unless technical dependencies require minor adjustment:

1. design tokens
2. component primitives
3. map shell/home
4. search
5. destination details
6. route selection
7. route intelligence
8. navigation shell
9. speed/limit
10. camera markers
11. camera approach cards
12. restriction warnings
13. signal enforcement
14. upcoming sheet
15. Copilot
16. enforcement explorer
17. layers
18. report flow
19. trip summary/history
20. offline
21. settings
22. permissions
23. failure states
24. dark mode audit
25. landscape audit
26. accessibility audit
27. visual regression suite
28. final polish pass

After each stage:
compile + test + visually inspect.

---

# AF. FINAL UI ACCEPTANCE

Do not mark UI complete until:

- first-time user can navigate without tutorial
- app looks like a legitimate Play Store/App Store navigation product
- active navigation is clean
- speed/current limit are immediately readable
- cameras are visible on map
- next relevant camera distance is obvious
- irrelevant/opposite-direction cameras do not dominate
- restricted turns are unmistakable
- route intelligence is useful but compact
- Copilot is obvious
- camera explorer is reachable quickly
- dark mode is excellent
- landscape works
- small screens work
- no placeholder UI remains
- visual regression tests exist
- screenshots have been manually inspected and polished

Do not settle for “functional.”

The UI must be both functional and polished.

BEGIN IMPLEMENTING THE UI STEP BY STEP.
