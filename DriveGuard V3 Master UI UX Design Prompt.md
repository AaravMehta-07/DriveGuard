# DRIVEGUARD V3 — MASTER UI/UX DESIGN PROMPT
## Google-Maps-Familiar, Cleaner, Enforcement-Aware Navigation Interface

This prompt supplements the main DriveGuard V3 engineering/build specification.

Treat the main build prompt as the source of truth for product features, architecture, backend, navigation, enforcement intelligence, cameras, signals, restrictions, routing, compliance logic and deployment.

This prompt is the source of truth for:

- user experience
- information hierarchy
- visual design
- screen structure
- interaction patterns
- navigation flow
- component behavior
- map presentation
- warning presentation
- accessibility
- driver distraction minimization
- aesthetics
- animation
- responsive behavior
- day/night mode
- Android/iOS consistency
- Android Auto/CarPlay UX where permitted

Do NOT ignore or simplify this specification.

Do NOT create a generic AI-generated dashboard.

Do NOT make the app look like an admin panel.

Do NOT overcrowd the navigation screen.

Do NOT make it look “cyberpunk,” “futuristic,” “gaming,” or excessively colorful.

The target experience is:

# Google Maps familiarity
+
# Apple Maps visual cleanliness
+
# Waze-like road awareness
+
# DriveGuard-specific compliance intelligence

A first-time user should understand the app immediately without needing a tutorial.

The UI should feel polished enough to be a real consumer navigation product.

---

# 1. PRIMARY UX PRINCIPLE

The user should feel:

> “This works like the navigation apps I already understand, but it gives me much better awareness of speed limits, cameras, traffic rules and challan-risk situations.”

The UI should NOT feel:

> “This is a complicated traffic-police dashboard.”

The product is primarily a navigation app.

Compliance intelligence should appear contextually.

Navigation remains the dominant experience.

---

# 2. CORE UX PRIORITIES

In order:

1. Current driving/navigation instruction
2. Road geometry / route
3. Speed limit
4. Current speed
5. Immediate legal/compliance danger
6. Upcoming relevant enforcement
7. ETA / remaining distance
8. Traffic
9. Secondary route intelligence
10. Community/nonessential information

Do not visually give equal priority to everything.

---

# 3. GLOBAL DESIGN LANGUAGE

Create an original DriveGuard design system.

Target feel:

- modern
- premium
- lightweight
- calm
- highly legible
- trustworthy
- efficient
- practical
- map-first
- familiar
- minimal

Avoid:

- excessive gradients
- neon colors
- glowing effects
- oversized cards
- glassmorphism everywhere
- excessive shadows
- giant corner radii on every component
- giant icons
- unnecessary animations
- complicated dashboards
- floating controls everywhere
- visually noisy maps
- excessive borders
- excessive text

Use a restrained design.

---

# 4. GOOGLE MAPS FAMILIARITY WITHOUT COPYING

The app may use interaction patterns familiar from mainstream navigation products:

- full-screen map
- floating rounded search field
- bottom sheets
- floating map controls
- route alternatives on map
- bottom ETA bar
- top navigation instruction card
- current-location button
- map layers button
- expandable destination/search sheet
- swipeable route details

But:

DO NOT copy Google Maps pixel-for-pixel.

DO NOT copy proprietary icons/assets.

DO NOT duplicate exact color palette.

DO NOT clone exact spacing/geometry.

DriveGuard must have an independent identity.

---

# 5. APP INFORMATION ARCHITECTURE

The consumer app should have only a small number of major areas.

Primary experiences:

1. Map / Home
2. Search
3. Destination Details
4. Route Selection
5. Active Navigation
6. DriveGuard Copilot
7. Trip Summary / History
8. Saved Places
9. Settings

Secondary content should usually appear as bottom sheets rather than separate screens.

Avoid bottom navigation with 5–7 permanent tabs unless absolutely justified.

The map should remain the central interface.

---

# 6. HOME SCREEN

On app launch:

show full-screen map immediately.

No long splash screen.

No mandatory account signup.

No onboarding carousel blocking the app.

Guest mode should work immediately.

Top:

large floating search field:

`Where to?`

Within or beside search field:

- search icon
- microphone icon if voice search available
- profile/avatar or compact menu button

Below or within lower map region:

quick destinations:

- Home
- Work
- recent places

Primary DriveGuard secondary action:

`Start DriveGuard`

This enters Copilot Mode without destination.

Keep this button obvious but not dominant over search.

---

# 7. HOME MAP

On the normal browsing map, show:

- current location
- useful road labels
- traffic if enabled
- major verified camera markers
- signal enforcement according to zoom
- limited compliance icons based on zoom

Do NOT show every single traffic signal at city zoom.

Use dynamic visibility.

At low zoom:

- cluster cameras
- hide ordinary signals
- show only major closures/restrictions

At high zoom:

- individual cameras
- relevant signals
- restricted-turn markers
- detailed road context

---

# 8. SEARCH BAR DESIGN

Search bar should:

- float above map
- use strong contrast
- have comfortable touch height
- show placeholder `Where to?`
- open instantly
- use native-feeling animation into expanded search state

Do not create tiny search field.

Do not hide search behind a menu.

---

# 9. SEARCH SCREEN

When search activates:

show:

TOP:
- back button
- focused search field
- microphone

BODY:

First:
- recent destinations

Then:
- Home
- Work
- saved/favorites

Then:
- search results/autocomplete

Search result row:

- relevant icon/category
- name
- locality
- distance where useful

Avoid excessive metadata.

Example:

`Jio World Drive`
`BKC, Mumbai`

not:

15 lines of POI metadata.

---

# 10. SEARCH LOADING

Autocomplete should feel immediate.

Use:

- subtle loading indicator
- skeleton rows only if delay is noticeable
- no giant spinner covering screen

If no results:

show concise useful empty state.

---

# 11. DESTINATION DETAILS

Selecting destination should return user to map.

Show destination marker.

Bottom sheet contains:

- destination name
- address/locality
- approximate travel time
- primary `Directions` button

Secondary actions only if useful:

- Save
- Share
- Call where appropriate from POI provider

Do not overcrowd.

---

# 12. ROUTE SELECTION SCREEN

After requesting directions:

show route overview on map.

Map should:

- fit origin + destination + alternatives
- highlight selected route strongly
- display alternatives more subtly
- show traffic where supported
- display relevant enforcement icons on/near selected route

Bottom sheet:

```text
Marine Drive

Recommended
39 min
24.6 km
ETA 10:52 AM

Moderate traffic

DriveGuard Route Intelligence
📷 6 speed cameras
🚦📷 2 signal enforcement
🚫 1 restricted movement
↕ 4 speed changes

[Preview]          [START]
```

The exact styling should be more polished than ASCII, but preserve this hierarchy.

---

# 13. ROUTE ALTERNATIVE CARDS

Route alternatives should be quickly selectable.

Show:

- ETA
- difference from recommended route
- distance
- toll indicator if applicable
- route confidence where appropriate

Do not make user open a separate page.

Tapping route on map or route card changes selection.

---

# 14. ROUTE INTELLIGENCE SUMMARY

This is a DriveGuard differentiator.

But keep it compact.

Default:

one compact row/card:

`🛡 Route Intelligence`

then useful counts.

Tap to expand.

Expanded view:

- enforcement
- speed changes
- restricted movements
- temporary restrictions
- route-data coverage/confidence

Do not dump every event by default.

---

# 15. ROUTE CAMERA VISIBILITY

Before starting:

all route-relevant cameras should be visible geographically.

Verified camera:

solid marker.

Probable:

slightly softer appearance.

Reported/unverified:

not shown by default unless user enables that layer.

Tap count or route intelligence:

highlight route cameras.

---

# 16. START BUTTON

The `START` button should be:

- visually strongest action
- thumb reachable
- clear
- large enough
- not oversized

Use DriveGuard accent color.

No competing primary CTA.

---

# 17. ACTIVE NAVIGATION SCREEN — MOST IMPORTANT SCREEN

This screen must be extremely disciplined.

Primary structure:

### TOP
Navigation instruction.

### CENTER
Map.

### LOWER MAP
Current speed + speed limit.

### CONTEXT STRIP
Next DriveGuard intelligence item.

### BOTTOM
ETA / remaining distance / arrival time.

Everything else is secondary.

---

# 18. TOP MANEUVER CARD

Top instruction card should display:

- maneuver icon
- distance
- action
- next road

Example:

```text
↰ 450 m
Turn left
Marine Drive
```

It should be easy to read at a glance.

Use large maneuver distance/action.

Road name slightly smaller.

Do not include unnecessary sentence-long instructions.

---

# 19. SECONDARY MANEUVER

Where navigation provider supports it:

show next-next maneuver in a much smaller secondary line.

Only when useful.

Example:

`Then keep right`

Do not make it compete with primary turn.

---

# 20. LANE GUIDANCE

Where provider supports reliable lane guidance:

show temporary lane guidance near maneuver.

Example:

```text
↑   ↑   ↗
    USE THESE
```

Use clear lane arrows.

Remove after maneuver.

---

# 21. NAVIGATION MAP CAMERA

Map orientation:

default driving perspective / heading-up.

Support:

- heading-up
- north-up via control
- overview

Vehicle indicator should be visually clear.

Active route must be dominant.

Alternative roads remain readable but de-emphasized.

---

# 22. ROAD COLORS

Active route should have strong contrast against base map.

Traffic can color route segments where supported.

Do not let camera icons overwhelm route line.

Night mode must preserve clear route differentiation.

---

# 23. CURRENT SPEED

Show current speed continuously during active drive.

Display prominently but secondary to maneuver.

Example:

`47 km/h`

Use smooth speed updates.

Avoid jumping values.

---

# 24. SPEED LIMIT

Show road-sign-like speed limit representation beside current speed.

Example:

```text
┌──────┐
│  50  │
└──────┘
LIMIT
```

Do not exactly clone proprietary road-sign graphics if unnecessary.

The representation should still be instantly understandable.

---

# 25. SPEED STATES

Normal:

speed value neutral.

Near/at warning threshold:

subtle attention.

Meaningful overspeed:

stronger warning.

Substantial overspeed:

high-visibility warning + voice/haptic.

Do NOT flash the whole screen continuously.

Do NOT create distracting red animations.

---

# 26. SPEED WARNING EXAMPLE

Normal:

```text
LIMIT 50
47 km/h
```

Overspeed:

```text
LIMIT 50
⚠ 62 km/h
```

Context alert:

`Reduce speed`

Use short language.

---

# 27. CAMERA MARKERS

Camera markers must be instantly recognizable.

Create original icons for:

- speed camera
- red-light camera
- combined enforcement
- average-speed zone
- unverified report

Verified camera markers should remain visible on map while navigating.

Do not make them gigantic.

---

# 28. CAMERA DISTANCE CARD

When a relevant camera is upcoming, show a compact contextual card.

Example:

```text
📷 Speed camera
620 m
Limit 50 km/h
```

This card should NOT cover navigation instructions.

It should be part of a dedicated DriveGuard context region.

---

# 29. CAMERA APPROACH STATES

Far:

small/nonintrusive.

Approaching:

slightly emphasized.

Overspeeding while approaching:

more prominent.

After passing:

remove upcoming card smoothly.

Do not repeatedly animate.

---

# 30. CAMERA VOICE WARNING UI SYNC

When voice says:

“Speed camera ahead in 600 metres. Limit 50.”

The on-screen card must display the same information.

No mismatch between audio and UI.

---

# 31. OPPOSITE DIRECTION CAMERA

Camera may remain visible on map.

But if irrelevant to driver:

- lower visual emphasis
- no upcoming card
- no voice warning

This visually reinforces the system's intelligence.

---

# 32. FLYOVER CAMERA

If camera exists on surface road below user:

do not display it as an upcoming event.

If visible geographically, use subdued marker due to road-level mismatch.

---

# 33. TRAFFIC SIGNAL MARKERS

Normal signal:

simple traffic-light marker.

Signal enforcement:

signal + enforcement indicator.

Keep icon language clear.

---

# 34. SIGNAL COUNTDOWN

Only display if real provider-backed current data exists.

If available:

example:

`🚦 Green 18s`

or appropriate provider-compatible design.

Never fake it.

Do not display a timer UI when no live data exists.

---

# 35. RESTRICTED TURN WARNING

This must get greater priority than a camera.

When approaching prohibited turn:

display strong temporary card:

```text
🚫 DO NOT TAKE NEXT LEFT
Restricted movement
120 m
```

Use voice simultaneously.

Avoid giant persistent full-screen takeover unless imminent.

---

# 36. CRITICAL WARNING STYLE

Critical road-rule warnings should:

- temporarily push ordinary context lower
- use clear icon
- use strong semantic contrast
- include simple action

Example:

`DO NOT ENTER`

not:

`Potential traffic compliance conflict detected`

Use human language.

---

# 37. ALERT PRIORITY UI

Only ONE primary DriveGuard alert card should be prominent.

If:

camera + speed + restricted turn happen simultaneously:

priority should likely be:

restricted turn
then severe overspeed
then camera

Secondary items can remain small.

Do not stack 4 warning cards.

---

# 38. UPCOMING STRIP

Create collapsible bottom sheet/strip.

Collapsed:

shows only next item.

Expanded:

```text
UPCOMING

📷 0.6 km   Speed camera · 50
🚦 1.4 km   Signal
🚫 2.1 km   No left turn
60  3.8 km  Speed limit 60
📷 5.2 km   Speed camera · 60
```

Use clean list rows.

No timeline graphic if it adds clutter.

---

# 39. BOTTOM NAVIGATION STATUS

During navigation bottom bar:

```text
39 min
17 km
10:14 AM
```

Optionally swipe/tap to expand trip details.

This should remain visually stable.

---

# 40. END NAVIGATION CONTROL

Do not put a dangerous huge “X” near primary driving actions.

Provide clearly discoverable:

- exit/end navigation
- route overview
- mute
- report

Keep secondary.

---

# 41. RECENTER BUTTON

If user pans map:

show recenter button.

After idle period optionally return to navigation view only if that is standard/safe behavior.

Do not fight the user while they inspect route.

---

# 42. ROUTE OVERVIEW

Tap overview:

camera zooms to show route.

Show `Recenter`/`Resume`.

Maintain active navigation.

---

# 43. MUTE

Provide simple voice icon.

States:

- full voice
- alerts only
- muted

Tap can cycle or open small sheet.

Do not bury this in Settings.

---

# 44. COPILOT MODE HOME ENTRY

Home screen:

`🛡 Start DriveGuard`

Tap once.

If permissions already granted:

Copilot starts immediately.

No unnecessary configuration wizard.

---

# 45. COPILOT MODE UI

Copilot is map-first.

No destination route.

Top compact status:

`DriveGuard Active`

Map follows current location.

Show:

- current road
- speed
- speed limit
- relevant upcoming camera
- signal enforcement
- direct no-entry/restriction warnings

Keep UI even simpler than navigation.

---

# 46. COPILOT EXAMPLE

```text
Netaji Subhash Road

           ●

LIMIT 50
47 km/h

📷 Speed camera
850 m
```

If user begins approaching restricted entry:

critical alert replaces camera card.

---

# 47. ENFORCEMENT EXPLORER

Dedicated camera browsing experience.

Entry from map layers/menu.

Title:

`Enforcement Map`

Map remains full-screen.

Top:

search.

Floating filter button.

Filters:

- Speed cameras
- Signal cameras
- Combined
- Average-speed
- Verified
- Reported
- Traffic signals
- Restrictions

Use chips/sheet.

---

# 48. ENFORCEMENT CAMERA DETAIL SHEET

Tap camera:

bottom sheet.

Show only useful user-facing information.

Example:

```text
Speed Camera
Eastern Express Highway

Southbound

Limit
50 km/h

Status
Verified

Last verified
3 days ago

Source
Multiple verified sources
```

Action:

`Show on route`

if route active.

Do not expose raw database fields.

---

# 49. CAMERA CLUSTERING

At low zoom:

cluster markers.

Examples:

`5`
`12`
`28`

Cluster should visually imply enforcement points.

Tapping cluster zooms naturally.

---

# 50. LAYERS BUTTON

One familiar layers control on map.

Open bottom sheet.

Sections:

### Map
Traffic
Satellite if provider supports

### DriveGuard
Speed cameras
Signal enforcement
Traffic signals
Restricted turns
No entry

### Optional
Challan hotspots
Parking
Community reports
Temporary restrictions

Do not make layers a separate settings page.

---

# 51. DEFAULT LAYERS

Default during normal browsing:

- traffic ON
- verified cameras ON
- signal enforcement ON
- restricted turns selectively ON
- ordinary signals dependent on zoom
- challan hotspots OFF
- reported cameras OFF

During navigation:

only route-relevant compliance markers should receive high emphasis.

---

# 52. CHALLAN HOTSPOT LAYER

When enabled:

use subtle heatmap.

Do not dominate road colors.

Tap hotspot:

show:

- common violation category
- aggregated event count/range
- confidence
- time period

Never imply camera exists unless verified separately.

---

# 53. TRIP SUMMARY

After arrival:

show compact trip summary.

Example:

```text
Trip complete

26.7 km
57 min

DriveGuard
2 speed warnings
1 restricted-turn warning
3 enforcement points passed
```

Optional:

`View details`

No celebratory gamification that encourages speed.

---

# 54. TRIP DETAIL

Can show:

- route
- duration
- distance
- compliance events
- warnings
- camera encounters

Keep this separate from active-driving UI.

---

# 55. HOME/WORK UI

Saved places should be immediately accessible below search.

Simple compact chips/cards.

Do not turn home screen into a list feed.

---

# 56. SETTINGS INFORMATION ARCHITECTURE

Keep settings categorized:

### Navigation
route preferences
tolls/highways

### DriveGuard Alerts
speed
camera
signal
turn restrictions
voice
haptics

### Map
layers
theme

### Vehicle
vehicle type

### Offline
Mumbai Compliance Pack

### Privacy
trip history
analytics
delete data

### About
legal
attribution
data sources

---

# 57. SETTINGS COMPONENT STYLE

Use standard mobile settings patterns.

Rows with:

- title
- short subtitle if needed
- switch / chevron

Do not make settings custom cards everywhere.

---

# 58. FIRST LAUNCH

First launch should be extremely short.

Sequence:

1. app loads map
2. concise explanation of location need
3. system permission
4. optional notification permission later, when relevant

Do not request everything immediately.

Do not require signup.

---

# 59. LOCATION PERMISSION COPY

Use useful copy:

> DriveGuard uses your location to provide navigation, speed-limit and road-rule alerts while you drive.

For background access:

explain Copilot/navigation need.

Do not use manipulative wording.

---

# 60. NOTIFICATION PERMISSION

Ask only when needed.

Example:

when enabling background Copilot.

---

# 61. LOGIN

Optional.

Sign-in useful for:

- sync
- favorites
- trip history
- community reputation

Allow:

`Continue without account`

prominently.

---

# 62. ERROR STATES

All errors should be understandable.

Examples:

No GPS:

`Location unavailable`
`Move to an open area or check Location Services.`

No internet:

`You're offline`
`Downloaded DriveGuard data is still available.`

Search provider unavailable:

`Search temporarily unavailable.`

Do not expose exception text.

---

# 63. DATA UNCERTAINTY UI

If speed limit unknown:

do NOT show `50` guessed.

Show:

`Limit unavailable`

or hide numeric limit.

If camera uncertain:

marker style indicates it.

If restriction uncertain:

do not use misleading “verified” styling.

---

# 64. COVERAGE COMMUNICATION

Do not constantly show scary disclaimers.

Use subtle source/status indicators.

Settings/about can explain:

> DriveGuard coverage varies by road and source.

During route selection:

optional:

`Route data coverage 96%`

Only when meaningful.

---

# 65. DAY MODE

Day map:

- light neutral roads
- clear road hierarchy
- strong route line
- readable labels
- subtle terrain/POI detail
- camera icons visible but not dominant

Do not make map stark white everywhere.

---

# 66. NIGHT MODE

Night mode should be genuinely comfortable.

Requirements:

- dark charcoal/navy-neutral map base
- not pure black everywhere
- muted minor roads
- strong route line
- readable road labels
- camera/restriction icons remain visible
- no blinding white cards

Navigation cards use dark surfaces.

---

# 67. COLOR SYSTEM

Create semantic palette.

Need:

- primary accent
- neutral text/backgrounds
- route color
- traffic states
- warning
- critical
- verified enforcement
- reported/unverified
- success/status

Do NOT use 15 random colors.

Never rely only on color.

Use icon + text + contrast.

---

# 68. BRAND COLOR

Choose one primary DriveGuard accent.

It should feel:

- trustworthy
- navigational
- modern

Avoid looking exactly like Google blue or Waze branding.

Use it for:

- primary CTA
- selected route
- active state
- relevant verified DriveGuard elements

But traffic/enforcement semantic colors can differ appropriately.

---

# 69. TYPOGRAPHY

Use platform-appropriate high-quality sans-serif.

Prefer native/system font unless strong reason otherwise.

Hierarchy:

navigation distance/action:
large

road name:
medium

speed:
large

speed limit:
clearly readable

body:
standard

helper:
smaller

Do not use very thin font weights.

---

# 70. NUMERIC LEGIBILITY

Speed, distance and ETA must be readable quickly.

Use tabular numerals where appropriate.

Avoid tiny unit labels.

---

# 71. ICONS

Use consistent icon family.

Stroke/fill treatment should be coherent.

Do not mix five icon libraries visibly.

Create custom SVGs where DriveGuard concepts need them.

---

# 72. SPACING

Use consistent spacing system.

Avoid:

- random 11px/17px/23px spacing everywhere
- huge empty areas
- cramped cards

Create shared tokens.

---

# 73. CORNER RADII

Use moderate consistent radii.

Search bar/bottom sheets can be rounded.

Do not make every UI component a pill.

---

# 74. SHADOWS

Use subtle elevation only where map overlays require separation.

Do not use giant blurred shadows.

---

# 75. BOTTOM SHEETS

Bottom sheets are central.

Support:

- collapsed
- medium
- expanded

Use clear drag handle.

Sheet should follow native-feeling physics.

Map should remain visible.

---

# 76. BOTTOM SHEET BEHAVIOR

Examples:

Destination details:
medium

Route selection:
medium

Camera details:
compact/medium

Upcoming route:
collapsed → medium

Search:
can expand almost full screen

Avoid stacking bottom sheets.

---

# 77. ANIMATIONS

Use short purposeful transitions.

Examples:

- sheet expand
- route selection transition
- camera card appearance
- warning change
- map recenter

Avoid:

- bouncing icons
- pulsing cameras continuously
- dramatic page transitions
- excessive parallax
- confetti

---

# 78. CAMERA MARKER ANIMATION

Do not animate every camera.

When camera becomes route-relevant:

a subtle one-time emphasis is enough.

---

# 79. CRITICAL WARNING ANIMATION

Maybe one short attention transition.

No flashing.

No repeated shaking.

Driver distraction is more important than visual drama.

---

# 80. RESPONSIVE MOBILE LAYOUT

Design first for typical portrait phones.

Support:

- compact Android phones
- large Android phones
- iPhones
- display cutouts
- dynamic islands/status areas
- gesture navigation areas

Never place critical controls under system gesture zones.

---

# 81. LANDSCAPE MODE

Support landscape navigation.

Rearrange:

maneuver card → side/top

ETA → side/bottom

speed → visible

map should gain space.

Do not just stretch portrait layout.

---

# 82. TABLETS / FOLDABLES

Use extra space intelligently.

Potential:

map + route/event side panel.

Do not simply scale all components larger.

---

# 83. ANDROID / IOS

Maintain one coherent DriveGuard identity while respecting platform conventions.

Android:

- Material-compatible interactions where useful
- Android back behavior
- permission patterns

iOS:

- navigation patterns
- safe areas
- sheets
- native gestures

Avoid making iOS look like an Android port or vice versa.

---

# 84. ANDROID AUTO

Follow official car templates.

Do NOT force phone UI onto head unit.

Prioritize:

- next maneuver
- route
- ETA
- speed limit where allowed
- critical DriveGuard alert
- camera distance if permitted
- safe report controls

Minimal interaction.

---

# 85. CARPLAY

Follow official Apple navigation templates/requirements.

Again:

do not recreate custom phone UI.

DriveGuard intelligence should fit within allowed navigation alerts.

---

# 86. ACCESSIBILITY

Meet strong accessibility standards.

Support:

- dynamic text scaling
- screen reader labels
- color contrast
- voice guidance
- large touch targets
- semantic icons
- reduce motion

Critical warnings must be understandable without relying on red color.

---

# 87. TOUCH TARGETS

Driving screen controls:

large enough for quick operation.

Do not make tiny map-layer or mute icons.

---

# 88. ONE-HANDED USE

Common pre-drive actions should be reachable near lower screen area.

But do not force all navigation controls into bottom-right crowding.

---

# 89. VISUAL PRIORITY OF CAMERAS

The camera is important but the road/navigation is more important.

Camera marker should never obscure:

- turn arrow
- user location
- lane guidance
- critical road label

Implement marker collision/priority.

---

# 90. SIGNAL CLUTTER CONTROL

At full Mumbai zoom:

hide normal traffic signals.

At neighborhood zoom:

show important signals.

During navigation:

show route-relevant upcoming signal.

---

# 91. CAMERA CLUTTER CONTROL

At low zoom:

clusters.

At medium:

individual high-confidence cameras.

At active navigation:

route-applicable cameras strongest.

Others subdued.

---

# 92. MAP LABEL CLUTTER

Reduce nonessential businesses/POIs while actively navigating.

Prioritize:

- road names
- destination
- major landmarks
- enforcement/compliance

---

# 93. START DRIVEGUARD BUTTON

Home secondary CTA.

Visual:

shield icon + `Start DriveGuard`

Tap launches Copilot.

Long explanation not needed.

Small subtitle optional:

`Alerts without a destination`

---

# 94. COPILOT ACTIVE INDICATOR

Small persistent indicator:

`🛡 DriveGuard Active`

Do not show giant banner.

---

# 95. PASSENGER MODE / INTERACTION

If product supports passenger confirmation later:

ensure UI can distinguish passenger interaction safely.

Do not assume every device interaction means driver.

Follow platform automotive guidelines.

---

# 96. REPORT FLOW

Tap report.

Open safe bottom sheet with large category buttons:

Camera
Restriction
Closure
Police
Wrong speed limit
Map issue

One or two taps.

No typing while moving.

Detailed correction can happen after trip.

---

# 97. REPORT CONFIRMATION

After report:

small toast:

`Thanks — report received.`

Do not interrupt navigation.

---

# 98. TOASTS

Use sparingly.

Never cover critical speed/navigation information.

---

# 99. MODALS

Avoid modal dialogs during active navigation except truly critical issues.

Use sheets/toasts/context strips instead.

---

# 100. ROUTE INTELLIGENCE DETAILS

Expanded view should list in route order.

Example:

```text
Route Intelligence

0.8 km   📷 Speed camera · 50
2.1 km   🚫 No-left restriction
3.4 km   🚦📷 Signal enforcement
5.0 km   60 Speed limit
```

Tap item → map centers.

---

# 101. ROUTE SCANNER UX

When destination route is prepared:

do NOT show a fake long scanning animation.

Perform actual computation.

If quick:

show instantly.

If longer:

small progress indicator:

`Checking road rules…`

Then results.

---

# 102. ROUTE CONFIDENCE

Keep subtle.

Example:

`DriveGuard coverage: High`

or:

`Route rule coverage: 96%`

Detailed methodology behind info icon.

Do not overwhelm normal users with confidence math.

---

# 103. VERIFIED BADGES

Use status:

`Verified`

sparingly.

Don't place badges beside every map marker.

Details sheet is better.

---

# 104. UNVERIFIED MARKERS

Reported marker visually distinct.

Default layer can hide them.

This protects trust.

---

# 105. MAP CAMERA TAP

Tap marker should:

- slightly select/highlight marker
- open bottom sheet
- keep map centered enough to see surrounding road

Do not jump to a separate full screen.

---

# 106. SPEED LIMIT UNKNOWN

Show perhaps:

`--`

with small:

`Limit unavailable`

Do not infer from nearby road unless engine actually supports confidence and explicit status.

---

# 107. SPEED LIMIT CHANGE

Upcoming road event can appear as:

`40 in 300 m`

Then after crossing segment:

new current speed limit.

Keep intuitive.

---

# 108. NOTIFICATION UI

Background Copilot can use persistent Android notification.

Example:

```text
DriveGuard Active
Current limit: 50 km/h
Next enforcement: 1.2 km
```

Do not update notification every second unnecessarily.

---

# 109. LOCK SCREEN

Where platform permits navigation lock-screen activity:

show only critical information.

Respect privacy.

---

# 110. ARRIVAL EXPERIENCE

Near destination:

reduce camera/event prominence unless critical.

Navigation instruction:

`Destination is on the left`

Then:

`You’ve arrived`

Trip summary available afterward.

---

# 111. EMPTY TRIP HISTORY

Simple:

`No trips yet`

No elaborate illustrations necessary.

---

# 112. HISTORY PRIVACY

Allow:

- clear individual trip
- clear all
- disable history

Make easy.

---

# 113. SAVED PLACES

Simple list.

Search + rename + delete.

No complex collections initially unless needed.

---

# 114. DOWNLOAD MUMBAI PACK

Offline screen:

```text
Mumbai Compliance Pack

Cameras
Signals
Road restrictions
Speed-limit data
Temporary restrictions

Updated: Today
Size: ...
[Download]
```

After:

`Downloaded`

Show freshness.

---

# 115. STALE OFFLINE PACK

If stale:

subtle warning:

`Update recommended`

Do not block navigation.

---

# 116. LOADING MAP

Use immediate background map loading.

If provider takes time:

show neutral map surface + location loading indicator.

No full white page.

---

# 117. MAP PROVIDER ATTRIBUTION

Always show required attribution legibly.

Do not hide it.

Integrate elegantly.

---

# 118. PRIVACY INDICATORS

When location actively used in Copilot/navigation:

state should be clear enough but not distracting.

Settings should explain tracking state.

---

# 119. PERFORMANCE FEEL

UI must feel:

- immediate
- responsive
- no janky sheet movement
- no delayed taps
- no heavy animation
- smooth map at 60 FPS target

Profile real devices.

---

# 120. LOW-END DEVICE MODE

Consider reducing:

- marker density
- animations
- shadow complexity

Do not remove essential warnings.

---

# 121. CONNECTIVITY STATUS

Do not show permanent “online” indicator.

Only show offline/degraded state when relevant.

---

# 122. FATAL PROVIDER FAILURE

If navigation unavailable but Copilot/compliance data still available:

offer:

`Navigation unavailable`
`DriveGuard alerts can continue.`

Then:

`Start DriveGuard`

This prevents useless hard failure.

---

# 123. ROUTE PROVIDER ERROR

Do not display developer/provider names to normal user.

Use:

`Couldn't calculate a route.`

Retry.

---

# 124. LOCATION INACCURATE

If confidence poor:

small message:

`Improving GPS accuracy…`

Suppress unreliable compliance alerts.

---

# 125. MAP CAMERA ORIENTATION

Camera detail can show:

`Monitors southbound traffic`

with small directional indicator.

Do not overcomplicate with degrees.

---

# 126. CAMERA LIMIT

If speed limit unknown:

camera detail:

`Speed limit: Check posted signs`

Do not guess.

---

# 127. CAMERA STATUS

Possible UI:

`Verified`

`Reported`

`Status uncertain`

`No longer active`

Use natural labels.

---

# 128. SIGNAL STATUS

Traffic signal location is different from enforcement.

Be clear:

`Traffic signal`

vs

`Signal enforcement`

Never confuse them.

---

# 129. COMMUNITY POLICE REPORT

If used:

label as:

`Reported enforcement`

not:

`Police checkpoint guaranteed`

Age reports quickly.

---

# 130. USER TRUST COPY

Avoid sensational language.

Do not say:

`CAMERA TRAP`

Use:

`Speed camera`

`Signal enforcement`

`Restricted turn`

Trustworthy tone.

---

# 131. CHALLAN LANGUAGE

The product can reference challans in reporting/history/marketing, but live UI should focus on:

`road rule`

`restriction`

`speed limit`

`enforcement`

not constant:

`avoid ₹1500 fine`

That keeps product safety-oriented.

---

# 132. MAIN MAP MENU

Keep profile/menu simple.

Possible items:

- Saved
- Trips
- Offline maps
- Settings
- Help

Avoid hamburger full of 20 features.

---

# 133. QUICK ACTIONS

Only contextually useful.

Do not place buttons like:

AI Assistant
Dashboard
Stats
Community
Reports
Explore
Safety
Feed

all on home.

The map/search is the product.

---

# 134. NO SOCIAL FEED

Do not create social/community feed.

Crowdsourcing should operate quietly behind reporting/verification.

---

# 135. NO GAMIFICATION

Do not reward speeding or “camera spotting.”

Avoid:

- points for passing cameras
- streaks
- speed leaderboards

If reputation exists for data reporting, keep behind scenes or modest.

---

# 136. DESIGN TOKENS

Create shared design tokens:

- colors
- typography
- spacing
- radii
- elevation
- icon sizes
- control heights
- animation durations

Use across Flutter/native/web consumer surfaces.

Admin can have separate utilitarian design system.

---

# 137. COMPONENT LIBRARY

Create reusable consumer components including:

- SearchBar
- MapControlButton
- NavigationManeuverCard
- SpeedPanel
- SpeedLimitBadge
- DriveGuardAlertCard
- EnforcementMarker
- SignalMarker
- RouteIntelligenceSummary
- RouteEventRow
- DestinationBottomSheet
- RouteSelectionSheet
- CameraDetailSheet
- LayerSheet
- CopilotStatus
- ETAFooter
- RestrictionWarning
- OfflineStatusBanner
- PermissionPrompt

Do not duplicate component code per screen.

---

# 138. COMPONENT STATES

Each reusable component must define:

- normal
- pressed
- disabled
- loading
- error
- selected
- dark mode

Where relevant:

- critical
- warning
- info

---

# 139. SKELETONS

Use subtle skeleton loading only for content rows/sheets.

Do not skeleton the navigation map excessively.

---

# 140. DESIGN REVIEW REQUIREMENT

Before considering UI complete:

review every major screen at:

- 320px-ish narrow phone
- common 360–390px Android
- modern iPhone width
- large phone
- landscape

Fix clipping.

---

# 141. SCREENSHOT/GOLDEN TESTS

Create golden UI tests for:

- home light
- home dark
- search
- destination
- route selection
- navigation normal
- navigation speed warning
- camera approach
- prohibited turn
- Copilot
- camera explorer
- camera details
- settings

Use stable synthetic data.

---

# 142. VISUAL REGRESSION

UI changes should fail golden tests when major components shift unexpectedly.

Update baselines intentionally.

---

# 143. DEVICE TESTING

Test on:

- lower-mid Android
- current Android flagship
- iPhone simulator/device where available

Verify:

- map performance
- touch latency
- text size
- night mode
- bottom sheets
- camera marker density

---

# 144. USER FLOW TEST — ZERO LEARNING

Scenario:

new user installs app.

Without tutorial:

1. finds search
2. searches destination
3. sees routes
4. selects route
5. sees camera count
6. taps START
7. understands speed limit/current speed
8. understands camera warning
9. finishes trip

If tester hesitates significantly because UI is unclear:

iterate.

---

# 145. USER FLOW TEST — COPILOT

Home screen.

User sees:

`Start DriveGuard`

Tap.

Immediately understands:

- it is active
- current speed
- speed limit
- next relevant enforcement

PASS only if obvious.

---

# 146. USER FLOW TEST — CAMERA EXPLORER

User wants to know camera locations around Mumbai.

From main map:

reach camera/enforcement view in <= 2 obvious actions.

Can visually see verified camera markers.

Tap camera.

Understand:

- type
- direction
- limit
- verification

PASS.

---

# 147. USER FLOW TEST — WRONG TURN

During navigation:

restricted-left warning should be unmistakable.

User must understand:

`DO NOT TAKE NEXT LEFT`

within less than one second of glancing.

---

# 148. UI PERFORMANCE ACCEPTANCE

Navigation UI should not degrade because enforcement markers are added.

Use:

- marker culling
- clustering
- efficient map overlays
- route-corridor filtering

No visible frame drops under normal Mumbai density.

---

# 149. UI PRIORITY ACCEPTANCE

At any random screenshot during active drive, a reviewer should immediately identify:

1. next turn
2. route
3. speed / speed limit
4. important DriveGuard warning
5. ETA

If not:

redesign.

---

# 150. CLUTTER ACCEPTANCE TEST

Take screenshot in dense South Mumbai.

If:

- cameras overlap road names
- signals cover route
- cards obscure map
- 5 alerts visible

FAIL.

Reduce information.

---

# 151. AESTHETIC ACCEPTANCE TEST

The product must look like a credible app users would download from Google Play/App Store.

Reject:

- template-dashboard aesthetic
- bootstrap-like cards
- random gradients
- developer-looking map markers
- generic Material defaults with no polish
- inconsistent typography
- inconsistent spacing
- obvious AI-generated UI clutter

---

# 152. DESIGN INSPIRATION PRINCIPLE

Study CURRENT official screenshots/patterns from mainstream navigation products only as usability inspiration.

Do not copy exact proprietary design.

Focus on:

- familiar interaction model
- information hierarchy
- speed of use
- map-first interface

DriveGuard should visually stand on its own.

---

# 153. CONSUMER APP VS ADMIN

Do not reuse admin components inside mobile consumer UI.

Admin can be dense.

Consumer must remain minimal.

---

# 154. NO PLACEHOLDER FINAL UI

Temporary scaffolding is allowed during implementation.

Before final completion:

replace:

- generic icons
- placeholder colors
- lorem ipsum
- ugly debug cards
- default map pins
- TODO screens

with final polished consumer components.

---

# 155. UI AUDIT BEFORE COMPLETION

Perform a full UI audit.

Review:

Home
Search
Destination
Routes
Navigation
Camera approach
Overspeed
Restricted turn
Signals
Copilot
Enforcement Map
Camera details
Layers
Trip summary
Offline
Settings
Permissions
Errors
Dark mode
Landscape

List defects.

Fix them.

Do not simply state UI is good.

---

# 156. FINAL NAVIGATION VISUAL TARGET

Normal navigation should conceptually feel like:

```text
┌──────────────────────────────┐
│ ↰ 450 m                     │
│ Turn left · Marine Drive    │
├──────────────────────────────┤
│                              │
│            ROUTE             │
│              ↑               │
│              │   📷          │
│              │               │
│             ●                │
│                              │
│                              │
│  ┌────┐                      │
│  │ 50 │   47 km/h            │
│  └────┘                      │
│                              │
│ 📷 Speed camera · 620 m      │
│    Limit 50 km/h             │
├──────────────────────────────┤
│ 39 min    17 km    10:14 AM │
└──────────────────────────────┘
```

The implementation must be polished, responsive and visually superior to this crude diagram.

The diagram only communicates hierarchy.

---

# 157. CRITICAL-WARNING VISUAL TARGET

Concept:

```text
┌──────────────────────────────┐
│ 🚫 DO NOT TAKE NEXT LEFT    │
│ Restricted movement · 120 m │
├──────────────────────────────┤
│                              │
│          NAVIGATION MAP      │
│                              │
│  LIMIT 50       42 km/h      │
│                              │
├──────────────────────────────┤
│ 31 min    12 km    10:02 AM │
└──────────────────────────────┘
```

Camera warnings become temporarily secondary.

---

# 158. CAMERA EXPLORER VISUAL TARGET

Concept:

```text
┌──────────────────────────────┐
│ 🔍 Search Mumbai            │
│                              │
│      📷        📷            │
│             12               │
│  🚦📷                        │
│                        📷    │
│                              │
│          ●                   │
│                              │
│ [Filters]          [Layers]  │
└──────────────────────────────┘
```

Minimal map chrome.

---

# 159. DESIGN DELIVERABLES

Create and maintain:

`docs/UI_UX_SPEC.md`

Include:

- screen map
- design tokens
- components
- states
- user flows
- alert priority
- map marker strategy
- responsive rules

Also create:

`docs/SCREEN_INVENTORY.md`

listing every consumer screen/sheet and its implementation status.

---

# 160. UI IMPLEMENTATION RULE

Do not respond by merely creating Figma-style descriptions.

Implement these screens in the actual Flutter/native application.

The user wants a working application.

---

# 161. FINAL UI DEFINITION OF DONE

UI is done only when:

- all primary flows work
- no dead buttons
- no placeholder consumer screens
- light/dark mode complete
- responsive on tested sizes
- navigation hierarchy correct
- cameras visible appropriately
- camera distance clear
- speed limit/current speed clear
- restricted turn warnings dominant
- Copilot clean
- route scanner useful
- map not cluttered
- accessibility checked
- golden tests added
- major visual defects fixed
- app looks production ready

---

# 162. FINAL PRODUCT EXPERIENCE

The visual product should make a driver think:

> “This feels immediately familiar. I can just use it instead of Google Maps.”

But within the first drive they should also notice:

> “It tells me the speed limit much more clearly.”

> “It shows cameras directly on the map.”

> “It tells me how far the next relevant camera is.”

> “It warns me before restricted turns.”

> “It understands signals and enforcement.”

> “And none of that makes the map messy.”

That is the required design outcome.

---

# 163. EXECUTION

Use this UI/UX specification together with the main DriveGuard V3 master build prompt.

Treat both as binding.

If a technical implementation conflicts with usability:

find a solution that preserves safety and functionality while keeping the consumer interface minimal.

Do not skip polishing because functionality exists.

Build the full consumer UI.

Test it.

Inspect it visually.

Fix clutter.

Fix alignment.

Fix spacing.

Fix poor hierarchy.

Fix ugly default components.

Fix inconsistent dark mode.

Fix overlapping map elements.

Fix confusing alert states.

Continue iterating until DriveGuard looks and feels like a credible premium navigation app.

BEGIN.
