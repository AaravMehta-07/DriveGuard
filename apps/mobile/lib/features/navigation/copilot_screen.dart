import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:flutter_map/flutter_map.dart';
import 'package:latlong2/latlong.dart';
import '../../core/compliance/viewport_insets.dart';
import '../../core/theme/tokens.dart';
import '../../core/theme/typography.dart';
import '../../shared/widgets/copilot_active_pill.dart';
import '../../shared/widgets/current_speed_display.dart';
import '../../shared/widgets/map_controls.dart';
import '../../shared/widgets/speed_limit_badge.dart';

/// DriveGuard Copilot Mode Screen.
/// Follows vehicle position via GPS without entering a destination.
/// Displays current road name, current speed, speed limit, overspeed alerts,
/// upcoming camera warnings, and prohibited turn warnings.
/// Operates as background location service on Android/iOS.
class CopilotScreen extends ConsumerStatefulWidget {
  const CopilotScreen({super.key});

  @override
  ConsumerState<CopilotScreen> createState() => _CopilotScreenState();
}

class _CopilotScreenState extends ConsumerState<CopilotScreen> {
  double _currentSpeed = 48.0;
  int? _currentSpeedLimit = 50;
  String _currentRoad = 'Western Express Highway, Andheri East';
  String? _upcomingAlertText = 'Speed camera ahead in 750 m · 50 km/h limit';

  @override
  Widget build(BuildContext context) {
    final insets = MapViewportInsets.fromContext(context);

    return Scaffold(
      backgroundColor: DriveGuardColors.nightBackground,
      body: Stack(
        children: [
          // 1. Interactive Map Layer
          _buildMapLayer(),

          // 2. TOP: Status Pill & Current Road
          Positioned(
            top: insets.systemTopSafeArea + 16.0,
            left: 16.0,
            right: 16.0,
            child: Column(
              children: [
                const CopilotActivePill(),
                const SizedBox(height: 8),
                Container(
                  padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 10),
                  decoration: BoxDecoration(
                    color: DriveGuardColors.nightSurface.withOpacity(0.95),
                    borderRadius: BorderRadius.circular(DriveGuardRadii.medium),
                    border: Border.all(color: Colors.white.withOpacity(0.1)),
                  ),
                  child: Row(
                    children: [
                      const Icon(Icons.add_location_alt_rounded, color: DriveGuardColors.brandPrimary, size: 20),
                      const SizedBox(width: 8),
                      Expanded(
                        child: Text(
                          _currentRoad,
                          style: DriveGuardTypography.body.copyWith(
                            color: Colors.white,
                            fontWeight: FontWeight.w600,
                          ),
                          maxLines: 1,
                          overflow: TextOverflow.ellipsis,
                        ),
                      ),
                    ],
                  ),
                ),
              ],
            ),
          ),

          // 3. UPCOMING WARNING CARD (if any)
          if (_upcomingAlertText != null)
            Positioned(
              left: 16.0,
              right: 16.0,
              top: insets.systemTopSafeArea + 120.0,
              child: Container(
                padding: const EdgeInsets.all(16),
                decoration: BoxDecoration(
                  color: const Color(0xFF1E293B),
                  borderRadius: BorderRadius.circular(DriveGuardRadii.medium),
                  border: Border.all(color: DriveGuardColors.warningAmber.withOpacity(0.4)),
                  boxShadow: const [BoxShadow(color: Colors.black45, blurRadius: 12)],
                ),
                child: Row(
                  children: [
                    const Icon(Icons.camera_alt_rounded, color: DriveGuardColors.warningAmber, size: 28),
                    const SizedBox(width: 12),
                    Expanded(
                      child: Text(
                        _upcomingAlertText!,
                        style: DriveGuardTypography.body.copyWith(
                          color: Colors.white,
                          fontWeight: FontWeight.w600,
                        ),
                      ),
                    ),
                  ],
                ),
              ),
            ),

          // 4. LOWER-LEFT: Speed Limit Badge + Current Speed
          Positioned(
            left: 16.0,
            bottom: insets.systemBottomSafeArea + 24.0,
            child: Container(
              padding: const EdgeInsets.all(12.0),
              decoration: BoxDecoration(
                color: DriveGuardColors.nightSurface.withOpacity(0.95),
                borderRadius: BorderRadius.circular(DriveGuardRadii.medium),
                border: Border.all(color: Colors.white.withOpacity(0.1)),
              ),
              child: Row(
                mainAxisSize: MainAxisSize.min,
                children: [
                  SpeedLimitBadge(speedLimitKph: _currentSpeedLimit),
                  const SizedBox(width: 12),
                  CurrentSpeedDisplay(
                    speedKph: _currentSpeed,
                    speedLimitKph: _currentSpeedLimit,
                  ),
                ],
              ),
            ),
          ),

          // 5. RIGHT: Exit Copilot Button
          Positioned(
            right: 16.0,
            bottom: insets.systemBottomSafeArea + 24.0,
            child: FloatingActionButton.extended(
              backgroundColor: Colors.redAccent.shade700,
              icon: const Icon(Icons.stop_rounded, color: Colors.white),
              label: const Text('Stop Copilot', style: TextStyle(color: Colors.white, fontWeight: FontWeight.bold)),
              onPressed: () => Navigator.pop(context),
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildMapLayer() {
    return FlutterMap(
      options: const MapOptions(
        initialCenter: LatLng(19.0760, 72.8777),
        initialZoom: 15.0,
      ),
      children: [
        TileLayer(
          urlTemplate: 'https://tile.openstreetmap.org/{z}/{x}/{y}.png',
          userAgentPackageName: 'com.driveguard.app',
        ),
        MarkerLayer(
          markers: [
            Marker(
              point: const LatLng(19.0760, 72.8777),
              width: 44,
              height: 44,
              child: Container(
                decoration: const BoxDecoration(
                  color: DriveGuardColors.brandPrimary,
                  shape: BoxShape.circle,
                  boxShadow: [BoxShadow(color: Colors.black38, blurRadius: 8)],
                ),
                child: const Icon(Icons.shield_rounded, color: Colors.white, size: 24),
              ),
            ),
            Marker(
              point: const LatLng(19.0820, 72.8820),
              width: 36,
              height: 36,
              child: Container(
                decoration: BoxDecoration(
                  color: DriveGuardColors.verifiedGreen.withOpacity(0.9),
                  shape: BoxShape.circle,
                ),
                child: const Icon(Icons.camera_alt_rounded, color: Colors.white, size: 20),
              ),
            ),
          ],
        ),
      ],
    );
  }
}
