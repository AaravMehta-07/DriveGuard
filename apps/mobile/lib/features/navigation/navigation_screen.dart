import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../core/compliance/alert_arbitrator.dart';
import '../../core/compliance/viewport_insets.dart';
import '../../core/theme/tokens.dart';
import '../../core/theme/typography.dart';
import '../../shared/widgets/alert_card.dart';
import '../../shared/widgets/camera_approach_card.dart';
import '../../shared/widgets/current_speed_display.dart';
import '../../shared/widgets/eta_footer.dart';
import '../../shared/widgets/map_controls.dart';
import '../../shared/widgets/navigation_maneuver_card.dart';
import '../../shared/widgets/restriction_warning_card.dart';
import '../../shared/widgets/secondary_maneuver_hint.dart';
import '../../shared/widgets/speed_limit_badge.dart';

/// Active Navigation Screen for DriveGuard V3.
/// The core driving interface designed for minimal distraction and high legibility.
///
/// Permanent Structure:
/// - TOP: NavigationManeuverCard (arrow, distance, action, target road)
/// - CENTER: Map (heading-up navigation perspective)
/// - LOWER-LEFT: SpeedLimitBadge + CurrentSpeedDisplay
/// - CONTEXT: ONE primary DriveGuardAlertCard (P0 > P1 > P2 > P3)
/// - BOTTOM: ETAFooter (stable: remaining time · distance · arrival time)
/// - FLOATING: Recenter, Overview, Mute, Report controls
class NavigationScreen extends ConsumerStatefulWidget {

  const NavigationScreen({
    super.key,
    this.routeId,
    this.destinationName = 'Destination',
  });
  final String? routeId;
  final String destinationName;

  @override
  ConsumerState<NavigationScreen> createState() => _NavigationScreenState();
}

class _NavigationScreenState extends ConsumerState<NavigationScreen> {
  // Navigation State
  double _currentSpeedKph = 54.0;
  int? _currentSpeedLimitKph = 50;
  bool _isOverviewMode = false;
  int _audioMuteState = 0; // 0=full, 1=alerts-only, 2=muted

  // Mock Active Alert (managed by AlertArbitrator in real flow)
  DriveGuardAlert? _activeAlert = const DriveGuardAlert(
    id: 'cam_approach_1',
    severity: AlertSeverity.P2_MEDIUM,
    type: AlertType.CAMERA_APPROACH,
    title: 'Speed camera ahead · 50 km/h limit',
    subtitle: '620 m away on Western Express Highway',
    distanceMeters: 620,
    speedLimitKph: 50,
  );

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);

    // Dynamic viewport insets for map layout (Correction #30)
    final insets = MapViewportInsets.fromContext(
      context,
      topManeuverCardHeight: 120.0,
      bottomEtaFooterHeight: 72.0,
    );

    return Scaffold(
      backgroundColor: DriveGuardColors.nightBackground,
      body: Stack(
        children: [
          // 1. Full-screen Map Viewport
          _buildMapViewport(insets),

          // 2. TOP: Navigation Maneuver Card & Secondary Hint
          Positioned(
            top: insets.systemTopSafeArea + 12.0,
            left: 16.0,
            right: 16.0,
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.stretch,
              children: const [
                NavigationManeuverCard(
                  maneuverType: 'turn-left',
                  distanceText: '400 m',
                  actionText: 'Turn left onto',
                  roadName: 'Subhash Road / Vile Parle Station',
                ),
                SizedBox(height: 8.0),
                SecondaryManeuverHint(
                  maneuverType: 'straight',
                  hintText: 'Then continue straight for 1.2 km',
                ),
              ],
            ),
          ),

          // 3. LOWER-LEFT: Speed Limit Badge + Current Speed Display
          Positioned(
            left: 16.0,
            bottom: insets.totalBottomInset + 12.0,
            child: Container(
              padding: const EdgeInsets.all(12.0),
              decoration: BoxDecoration(
                color: DriveGuardColors.nightSurface.withOpacity(0.9),
                borderRadius: BorderRadius.circular(DriveGuardRadii.medium),
                border: Border.all(color: Colors.white.withOpacity(0.1)),
                boxShadow: const [
                  BoxShadow(color: Colors.black38, blurRadius: 12.0),
                ],
              ),
              child: Row(
                mainAxisSize: MainAxisSize.min,
                children: [
                  SpeedLimitBadge(speedLimitKph: _currentSpeedLimitKph),
                  const SizedBox(width: 12.0),
                  CurrentSpeedDisplay(
                    speedKph: _currentSpeedKph,
                    speedLimitKph: _currentSpeedLimitKph,
                  ),
                ],
              ),
            ),
          ),

          // 4. CONTEXT / CENTER-LOWER: Single Primary DriveGuard Alert Card
          if (_activeAlert != null)
            Positioned(
              left: 16.0,
              right: 16.0,
              bottom: insets.totalBottomInset + 96.0,
              child: _buildPrimaryAlertCard(_activeAlert!),
            ),

          // 5. FLOATING CONTROLS (Right Column)
          Positioned(
            right: 16.0,
            bottom: insets.totalBottomInset + 12.0,
            child: Column(
              mainAxisSize: MainAxisSize.min,
              children: [
                if (_isOverviewMode)
                  MapRecenterButton(
                    onPressed: () => setState(() => _isOverviewMode = false),
                  )
                else
                  MapOverviewButton(
                    onPressed: () => setState(() => _isOverviewMode = true),
                  ),
                const SizedBox(height: 12.0),
                MapMuteButton(
                  muteState: _audioMuteState,
                  onPressed: () => setState(
                    () => _audioMuteState = (_audioMuteState + 1) % 3,
                  ),
                ),
                const SizedBox(height: 12.0),
                MapReportButton(
                  onPressed: _showReportingSheet,
                ),
              ],
            ),
          ),

          // 6. BOTTOM: ETA Footer
          Positioned(
            left: 0,
            right: 0,
            bottom: 0,
            child: Container(
              padding: EdgeInsets.only(bottom: insets.systemBottomSafeArea),
              decoration: BoxDecoration(
                color: DriveGuardColors.nightSurface,
                border: Border(
                  top: BorderSide(color: Colors.white.withOpacity(0.1)),
                ),
              ),
              child: ETAFooter(
                remainingMinutes: 32,
                remainingDistanceKm: 14.2,
                estimatedArrivalText: '10:45 AM',
                onEndNavigationPressed: _confirmEndNavigation,
              ),
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildMapViewport(MapViewportInsets insets) {
    return Container(
      color: const Color(0xFF0F172A),
      child: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            const Icon(
              Icons.navigation_rounded,
              size: 64,
              color: DriveGuardColors.brandPrimary,
            ),
            const SizedBox(height: 12),
            Text(
              'DriveGuard Map Viewport',
              style: DriveGuardTypography.body.copyWith(color: Colors.white70),
            ),
            const SizedBox(height: 4),
            Text(
              'Heading Up Navigation Mode · Provider Agnostic',
              style: DriveGuardTypography.secondaryMeta.copyWith(
                color: Colors.white38,
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildPrimaryAlertCard(DriveGuardAlert alert) {
    switch (alert.type) {
      case AlertType.CAMERA_APPROACH:
        return CameraApproachCard(
          distanceMeters: alert.distanceMeters ?? 500,
          speedLimitKph: alert.speedLimitKph ?? 50,
          roadName: 'Western Express Highway',
        );
      case AlertType.PROHIBITED_MANEUVER:
      case AlertType.NO_ENTRY:
        return RestrictionWarningCard(
          warningTitle: 'DO NOT TAKE NEXT LEFT',
          distanceMeters: alert.distanceMeters ?? 120,
          restrictionDetail: 'Verified prohibited left turn',
        );
      default:
        return DriveGuardAlertCard(
          title: alert.title,
          subtitle: alert.subtitle,
          severity: alert.severity,
          type: alert.type,
          distanceMeters: alert.distanceMeters,
        );
    }
  }

  void _showReportingSheet() {
    showModalBottomSheet(
      context: context,
      backgroundColor: DriveGuardColors.nightSurface,
      shape: const RoundedRectangleBorder(
        borderRadius: BorderRadius.vertical(top: Radius.circular(20)),
      ),
      builder: (context) => Padding(
        padding: const EdgeInsets.all(24.0),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            Text(
              'Report Road Issue',
              style: DriveGuardTypography.navigationAction.copyWith(
                color: Colors.white,
              ),
            ),
            const SizedBox(height: 16),
            Wrap(
              spacing: 12,
              runSpacing: 12,
              children: [
                _reportChip('📷 Speed Camera'),
                _reportChip('🚦 Signal Camera'),
                _reportChip('🚫 Restricted Turn'),
                _reportChip('⛔ No Entry'),
                _reportChip('🚧 Road Work'),
                _reportChip('⚠️ Hazard'),
              ],
            ),
          ],
        ),
      ),
    );
  }

  Widget _reportChip(String label) {
    return ActionChip(
      label: Text(label, style: const TextStyle(color: Colors.white)),
      backgroundColor: DriveGuardColors.nightCard,
      onPressed: () {
        Navigator.pop(context);
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(
            content: Text('Thanks — report submitted for verification'),
            duration: Duration(seconds: 2),
          ),
        );
      },
    );
  }

  void _confirmEndNavigation() {
    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        backgroundColor: DriveGuardColors.nightSurface,
        title: const Text(
          'End Navigation?',
          style: TextStyle(color: Colors.white),
        ),
        content: const Text(
          'Are you sure you want to stop current navigation?',
          style: TextStyle(color: Colors.white70),
        ),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(context),
            child: const Text('Resume'),
          ),
          TextButton(
            onPressed: () {
              Navigator.pop(context);
              Navigator.pop(context); // Return to home
            },
            child: const Text('End', style: TextStyle(color: Colors.redAccent)),
          ),
        ],
      ),
    );
  }
}
