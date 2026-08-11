import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';
import '../../core/compliance/viewport_insets.dart';
import '../../core/theme/tokens.dart';
import '../../core/theme/typography.dart';
import '../../shared/widgets/primary_drive_button.dart';

/// Navigation Home Screen for DriveGuard V3.
/// Full-screen map with floating search bar, quick destinations (Home/Work),
/// and "Start DriveGuard" Copilot mode CTA.
class HomeScreen extends ConsumerStatefulWidget {
  const HomeScreen({super.key});

  @override
  ConsumerState<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends ConsumerState<HomeScreen> {
  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final insets = MapViewportInsets.fromContext(context);

    return Scaffold(
      backgroundColor: DriveGuardColors.nightBackground,
      body: Stack(
        children: [
          // 1. Full-screen Map Layer
          _buildMapLayer(),

          // 2. TOP: Floating Search Bar ("Where to?")
          Positioned(
            top: insets.systemTopSafeArea + 16.0,
            left: 16.0,
            right: 16.0,
            child: GestureDetector(
              onTap: () => context.push('/search'),
              child: Container(
                height: 52.0,
                padding: const EdgeInsets.symmetric(horizontal: 16.0),
                decoration: BoxDecoration(
                  color: DriveGuardColors.nightSurface,
                  borderRadius: BorderRadius.circular(DriveGuardRadii.large),
                  border: Border.all(color: Colors.white.withOpacity(0.1)),
                  boxShadow: const [
                    BoxShadow(color: Colors.black45, blurRadius: 16.0, offset: Offset(0, 4)),
                  ],
                ),
                child: Row(
                  children: [
                    const Icon(Icons.search_rounded, color: DriveGuardColors.brandPrimary, size: 24),
                    const SizedBox(width: 12),
                    Expanded(
                      child: Text(
                        'Where to?',
                        style: DriveGuardTypography.body.copyWith(
                          color: DriveGuardColors.nightTextSecondary,
                          fontSize: 16,
                          fontWeight: FontWeight.w500,
                        ),
                      ),
                    ),
                    IconButton(
                      icon: const Icon(Icons.mic_rounded, color: Colors.white70, size: 22),
                      onPressed: () {},
                      tooltip: 'Voice Search',
                    ),
                  ],
                ),
              ),
            ),
          ),

          // 3. RIGHT: Map Controls (Layers, Explorer, Recenter)
          Positioned(
            right: 16.0,
            top: insets.systemTopSafeArea + 84.0,
            child: Column(
              children: [
                _buildFloatingButton(
                  icon: Icons.layers_rounded,
                  tooltip: 'Map Layers',
                  onTap: () => _showLayersSheet(context),
                ),
                const SizedBox(height: 12),
                _buildFloatingButton(
                  icon: Icons.explore_rounded,
                  tooltip: 'Enforcement Explorer',
                  onTap: () => context.push('/enforcement-explorer'),
                ),
                const SizedBox(height: 12),
                _buildFloatingButton(
                  icon: Icons.my_location_rounded,
                  tooltip: 'Recenter',
                  onTap: () {},
                ),
              ],
            ),
          ),

          // 4. BOTTOM: Quick Places & Copilot Mode CTA
          Positioned(
            left: 16.0,
            right: 16.0,
            bottom: insets.systemBottomSafeArea + 16.0,
            child: Column(
              mainAxisSize: MainAxisSize.min,
              crossAxisAlignment: CrossAxisAlignment.stretch,
              children: [
                // Quick Destination Cards
                Row(
                  children: [
                    Expanded(
                      child: _quickPlaceCard(
                        icon: Icons.home_rounded,
                        label: 'Home',
                        subtitle: 'Bandra West',
                        onTap: () => context.push('/route-selection?dest=Home'),
                      ),
                    ),
                    const SizedBox(width: 12),
                    Expanded(
                      child: _quickPlaceCard(
                        icon: Icons.work_rounded,
                        label: 'Work',
                        subtitle: 'BKC Annex',
                        onTap: () => context.push('/route-selection?dest=Work'),
                      ),
                    ),
                  ],
                ),
                const SizedBox(height: 12),

                // Primary "Start DriveGuard" (Copilot Mode) Button
                PrimaryDriveButton(
                  label: 'Start DriveGuard',
                  subtitle: 'Copilot mode · No destination needed',
                  onPressed: () => context.push('/copilot'),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildMapLayer() {
    return Container(
      color: const Color(0xFF0B132B),
      child: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            const Icon(Icons.map_rounded, size: 80, color: Colors.white12),
            const SizedBox(height: 12),
            Text(
              'DriveGuard Mumbai Map',
              style: DriveGuardTypography.navigationAction.copyWith(color: Colors.white38),
            ),
            const SizedBox(height: 4),
            Text(
              'Speed limits · Verified cameras · Prohibited turns',
              style: DriveGuardTypography.secondaryMeta.copyWith(color: Colors.white24),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildFloatingButton({required IconData icon, required String tooltip, required VoidCallback onTap}) {
    return Container(
      width: 48,
      height: 48,
      decoration: BoxDecoration(
        color: DriveGuardColors.nightSurface,
        shape: BoxShape.circle,
        border: Border.all(color: Colors.white.withOpacity(0.1)),
        boxShadow: const [BoxShadow(color: Colors.black38, blurRadius: 8)],
      ),
      child: IconButton(
        icon: Icon(icon, color: Colors.white, size: 22),
        onPressed: onTap,
        tooltip: tooltip,
      ),
    );
  }

  Widget _quickPlaceCard({
    required IconData icon,
    required String label,
    required String subtitle,
    required VoidCallback onTap,
  }) {
    return InkWell(
      onTap: onTap,
      borderRadius: BorderRadius.circular(DriveGuardRadii.medium),
      child: Container(
        padding: const EdgeInsets.symmetric(horizontal: 16.0, vertical: 12.0),
        decoration: BoxDecoration(
          color: DriveGuardColors.nightSurface.withOpacity(0.95),
          borderRadius: BorderRadius.circular(DriveGuardRadii.medium),
          border: Border.all(color: Colors.white.withOpacity(0.08)),
        ),
        child: Row(
          children: [
            Icon(icon, color: DriveGuardColors.brandPrimary, size: 24),
            const SizedBox(width: 12),
            Expanded(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                mainAxisSize: MainAxisSize.min,
                children: [
                  Text(label, style: DriveGuardTypography.body.copyWith(color: Colors.white, fontWeight: FontWeight.w600)),
                  Text(subtitle, style: DriveGuardTypography.secondaryMeta.copyWith(color: DriveGuardColors.nightTextSecondary)),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }

  void _showLayersSheet(BuildContext context) {
    showModalBottomSheet(
      context: context,
      backgroundColor: DriveGuardColors.nightSurface,
      shape: const RoundedRectangleBorder(borderRadius: BorderRadius.vertical(top: Radius.circular(20))),
      builder: (context) => Padding(
        padding: const EdgeInsets.all(24.0),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text('Map Layers', style: DriveGuardTypography.navigationAction.copyWith(color: Colors.white)),
            const SizedBox(height: 16),
            SwitchListTile(
              title: const Text('Speed Cameras', style: TextStyle(color: Colors.white)),
              subtitle: const Text('Verified speed enforcement points', style: TextStyle(color: Colors.white54)),
              value: true,
              onChanged: (v) {},
            ),
            SwitchListTile(
              title: const Text('Signal Enforcement', style: TextStyle(color: Colors.white)),
              subtitle: const Text('Red-light camera junctions', style: TextStyle(color: Colors.white54)),
              value: true,
              onChanged: (v) {},
            ),
            SwitchListTile(
              title: const Text('Turn Restrictions', style: TextStyle(color: Colors.white)),
              subtitle: const Text('No-left, no-right, no-U-turn markers', style: TextStyle(color: Colors.white54)),
              value: true,
              onChanged: (v) {},
            ),
          ],
        ),
      ),
    );
  }
}
