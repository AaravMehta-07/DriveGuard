import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';
import '../../core/compliance/viewport_insets.dart';
import '../../core/theme/tokens.dart';
import '../../core/theme/typography.dart';
import '../../shared/widgets/primary_drive_button.dart';
import '../../shared/widgets/route_intelligence_summary.dart';

/// Route Selection & Intelligence Screen for DriveGuard V3.
/// Displays destination details, candidate routes (Recommended, Fastest, DriveGuard Route),
/// traffic state, ETA, distance, and Route Intelligence summary (camera count, signal count,
/// turn restrictions, speed limit changes, active closures, and coverage %).
class RouteSelectionScreen extends ConsumerStatefulWidget {

  const RouteSelectionScreen({
    super.key,
    this.destinationName = 'Chhatrapati Shivaji Maharaj International Airport (BOM)',
  });
  final String destinationName;

  @override
  ConsumerState<RouteSelectionScreen> createState() => _RouteSelectionScreenState();
}

class _RouteSelectionScreenState extends ConsumerState<RouteSelectionScreen> {
  int _selectedRouteIndex = 0;

  // Mock candidate routes with route intelligence counts
  final List<Map<String, dynamic>> _candidateRoutes = [
    {
      'name': 'DriveGuard Compliant',
      'tag': 'RECOMMENDED',
      'duration': '34 min',
      'distance': '15.8 km',
      'eta': '10:48 AM',
      'traffic': 'MODERATE',
      'cameras': 4,
      'signals': 2,
      'restrictions': 0,
      'speed_changes': 3,
      'closures': 0,
      'coverage_percent': 98.5,
    },
    {
      'name': 'Western Express Hwy',
      'tag': 'FASTEST',
      'duration': '31 min',
      'distance': '14.2 km',
      'eta': '10:45 AM',
      'traffic': 'HEAVY',
      'cameras': 7,
      'signals': 4,
      'restrictions': 1,
      'speed_changes': 5,
      'closures': 0,
      'coverage_percent': 96.0,
    },
  ];

  @override
  Widget build(BuildContext context) {
    final insets = MapViewportInsets.fromContext(context);
    final selectedRoute = _candidateRoutes[_selectedRouteIndex];

    return Scaffold(
      backgroundColor: DriveGuardColors.nightBackground,
      appBar: AppBar(
        backgroundColor: DriveGuardColors.nightSurface,
        title: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text('To: ${widget.destinationName}', style: DriveGuardTypography.body.copyWith(color: Colors.white, fontWeight: FontWeight.bold)),
            Text('From: Current Location (Bandra West)', style: DriveGuardTypography.secondaryMeta.copyWith(color: DriveGuardColors.nightTextSecondary)),
          ],
        ),
        leading: IconButton(
          icon: const Icon(Icons.arrow_back_rounded, color: Colors.white),
          onPressed: () => Navigator.pop(context),
        ),
      ),
      body: Stack(
        children: [
          // 1. Map Viewport showing routes
          _buildRouteMap(),

          // 2. Bottom Route Options & Intelligence Sheet
          Positioned(
            left: 0,
            right: 0,
            bottom: 0,
            child: Container(
              padding: EdgeInsets.fromLTRB(16, 16, 16, insets.systemBottomSafeArea + 16),
              decoration: BoxDecoration(
                color: DriveGuardColors.nightSurface,
                borderRadius: const BorderRadius.vertical(top: Radius.circular(24)),
                border: Border(top: BorderSide(color: Colors.white.withOpacity(0.1))),
                boxShadow: const [BoxShadow(color: Colors.black54, blurRadius: 20)],
              ),
              child: Column(
                mainAxisSize: MainAxisSize.min,
                crossAxisAlignment: CrossAxisAlignment.stretch,
                children: [
                  // Drag Handle
                  Center(
                    child: Container(
                      width: 36,
                      height: 4,
                      decoration: BoxDecoration(
                        color: Colors.white24,
                        borderRadius: BorderRadius.circular(2),
                      ),
                    ),
                  ),
                  const SizedBox(height: 12),

                  // Route Option Cards
                  Row(
                    children: List.generate(_candidateRoutes.length, (index) {
                      final route = _candidateRoutes[index];
                      final isSelected = index == _selectedRouteIndex;
                      return Expanded(
                        child: GestureDetector(
                          onTap: () => setState(() => _selectedRouteIndex = index),
                          child: Container(
                            margin: EdgeInsets.only(right: index == 0 ? 8.0 : 0),
                            padding: const EdgeInsets.all(12),
                            decoration: BoxDecoration(
                              color: isSelected ? DriveGuardColors.brandPrimary.withOpacity(0.15) : DriveGuardColors.nightCard,
                              borderRadius: BorderRadius.circular(DriveGuardRadii.medium),
                              border: Border.all(
                                color: isSelected ? DriveGuardColors.brandPrimary : Colors.white.withOpacity(0.08),
                                width: isSelected ? 2.0 : 1.0,
                              ),
                            ),
                            child: Column(
                              crossAxisAlignment: CrossAxisAlignment.start,
                              children: [
                                Text(
                                  route['tag'],
                                  style: DriveGuardTypography.tinyAnnotation.copyWith(
                                    color: isSelected ? DriveGuardColors.brandPrimary : Colors.white54,
                                    fontWeight: FontWeight.bold,
                                  ),
                                ),
                                const SizedBox(height: 4),
                                Text(
                                  route['duration'],
                                  style: DriveGuardTypography.navigationAction.copyWith(color: Colors.white, fontWeight: FontWeight.bold),
                                ),
                                Text(
                                  '${route['distance']} · ${route['eta']}',
                                  style: DriveGuardTypography.secondaryMeta.copyWith(color: DriveGuardColors.nightTextSecondary),
                                ),
                              ],
                            ),
                          ),
                        ),
                      );
                    }),
                  ),
                  const SizedBox(height: 16),

                  // Route Intelligence Summary Card
                  RouteIntelligenceSummary(
                    speedCameraCount: selectedRoute['cameras'],
                    signalEnforcementCount: selectedRoute['signals'],
                    restrictedMovementCount: selectedRoute['restrictions'],
                    speedChangeCount: selectedRoute['speed_changes'],
                    activeClosureCount: selectedRoute['closures'],
                    coveragePercent: selectedRoute['coverage_percent'],
                  ),
                  const SizedBox(height: 16),

                  // Actions: Preview & START Navigation
                  Row(
                    children: [
                      OutlinedButton(
                        style: OutlinedButton.styleFrom(
                          side: BorderSide(color: Colors.white.withOpacity(0.2)),
                          padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 16),
                          shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
                        ),
                        onPressed: () => context.push('/route-preview'),
                        child: const Text('Preview', style: TextStyle(color: Colors.white, fontWeight: FontWeight.w600)),
                      ),
                      const SizedBox(width: 12),
                      Expanded(
                        child: PrimaryDriveButton(
                          label: 'START NAVIGATION',
                          subtitle: '${selectedRoute['duration']} · ${selectedRoute['distance']}',
                          onPressed: () => context.push('/navigation?routeId=${selectedRoute['name']}'),
                        ),
                      ),
                    ],
                  ),
                ],
              ),
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildRouteMap() {
    return Container(
      color: const Color(0xFF0F172A),
      child: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            const Icon(Icons.alt_route_rounded, size: 72, color: DriveGuardColors.brandPrimary),
            const SizedBox(height: 12),
            Text('Route Options & Intelligence', style: DriveGuardTypography.body.copyWith(color: Colors.white70)),
            const SizedBox(height: 4),
            Text('Scanning compliance along polyline...', style: DriveGuardTypography.secondaryMeta.copyWith(color: Colors.white38)),
          ],
        ),
      ),
    );
  }
}
