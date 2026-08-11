import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../core/compliance/viewport_insets.dart';
import '../../core/theme/tokens.dart';
import '../../core/theme/typography.dart';
import '../../shared/widgets/bottom_sheets/camera_detail_sheet.dart';

/// Dedicated Enforcement Explorer Screen for DriveGuard V3.
/// Allows drivers to browse, search, and inspect all known speed cameras,
/// red-light cameras, combined enforcement points, and traffic signals in Mumbai
/// without starting navigation.
class EnforcementExplorerScreen extends ConsumerStatefulWidget {
  const EnforcementExplorerScreen({super.key});

  @override
  ConsumerState<EnforcementExplorerScreen> createState() => _EnforcementExplorerScreenState();
}

class _EnforcementExplorerScreenState extends ConsumerState<EnforcementExplorerScreen> {
  String _selectedFilter = 'ALL';

  final List<String> _filters = [
    'ALL',
    'SPEED CAMERAS',
    'RED-LIGHT CAMERAS',
    'COMBINED',
    'AVERAGE SPEED ZONES',
    'SIGNALS',
    'RESTRICTIONS',
  ];

  @override
  Widget build(BuildContext context) {
    final insets = MapViewportInsets.fromContext(context);

    return Scaffold(
      backgroundColor: DriveGuardColors.nightBackground,
      appBar: AppBar(
        backgroundColor: DriveGuardColors.nightSurface,
        title: const Text('Mumbai Enforcement Explorer', style: TextStyle(color: Colors.white, fontWeight: FontWeight.bold)),
        leading: IconButton(
          icon: const Icon(Icons.arrow_back_rounded, color: Colors.white),
          onPressed: () => Navigator.pop(context),
        ),
      ),
      body: Stack(
        children: [
          // 1. Full-screen Enforcement Map
          _buildExplorerMap(),

          // 2. TOP: Horizontal Filter Chips
          Positioned(
            top: 12.0,
            left: 0,
            right: 0,
            child: SingleChildScrollView(
              scrollDirection: Axis.horizontal,
              padding: const EdgeInsets.symmetric(horizontal: 16),
              child: Row(
                children: _filters.map((filter) {
                  final isSelected = filter == _selectedFilter;
                  return Padding(
                    padding: const EdgeInsets.only(right: 8.0),
                    child: ChoiceChip(
                      label: Text(filter, style: TextStyle(color: isSelected ? Colors.white : Colors.white70, fontSize: 12, fontWeight: FontWeight.bold)),
                      selected: isSelected,
                      selectedColor: DriveGuardColors.brandPrimary,
                      backgroundColor: DriveGuardColors.nightSurface,
                      onSelected: (selected) {
                        if (selected) setState(() => _selectedFilter = filter);
                      },
                    ),
                  );
                }).toList(),
              ),
            ),
          ),

          // 3. BOTTOM: Sample Selected Camera Card Trigger
          Positioned(
            left: 16,
            right: 16,
            bottom: insets.systemBottomSafeArea + 16,
            child: Container(
              padding: const EdgeInsets.all(16),
              decoration: BoxDecoration(
                color: DriveGuardColors.nightSurface,
                borderRadius: BorderRadius.circular(DriveGuardRadii.medium),
                border: Border.all(color: Colors.white.withOpacity(0.1)),
                boxShadow: const [BoxShadow(color: Colors.black45, blurRadius: 12)],
              ),
              child: Row(
                children: [
                  Container(
                    padding: const EdgeInsets.all(10),
                    decoration: BoxDecoration(color: DriveGuardColors.verifiedGreen.withOpacity(0.2), borderRadius: BorderRadius.circular(8)),
                    child: const Icon(Icons.camera_alt_rounded, color: DriveGuardColors.verifiedGreen, size: 24),
                  ),
                  const SizedBox(width: 12),
                  Expanded(
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text('Fixed Speed Camera · 50 km/h', style: DriveGuardTypography.body.copyWith(color: Colors.white, fontWeight: FontWeight.bold)),
                        Text('Western Express Highway · Southbound carriageway', style: DriveGuardTypography.secondaryMeta.copyWith(color: DriveGuardColors.nightTextSecondary)),
                      ],
                    ),
                  ),
                  TextButton(
                    onPressed: _showCameraDetails,
                    child: const Text('Inspect', style: TextStyle(color: DriveGuardColors.brandPrimary, fontWeight: FontWeight.bold)),
                  ),
                ],
              ),
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildExplorerMap() {
    return Container(
      color: const Color(0xFF0F172A),
      child: const Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Icon(Icons.explore_rounded, size: 72, color: DriveGuardColors.brandPrimary),
            SizedBox(height: 12),
            Text('Mumbai Enforcement Map Viewport', style: TextStyle(color: Colors.white, fontWeight: FontWeight.bold, fontSize: 16)),
            SizedBox(height: 4),
            Text('Clustered geospatial camera layer · PostGIS query', style: TextStyle(color: Colors.white38, fontSize: 12)),
          ],
        ),
      ),
    );
  }

  void _showCameraDetails() {
    showModalBottomSheet(
      context: context,
      backgroundColor: DriveGuardColors.nightSurface,
      shape: const RoundedRectangleBorder(borderRadius: BorderRadius.vertical(top: Radius.circular(20))),
      builder: (context) => const CameraDetailBottomSheet(
        type: 'FIXED_SPEED',
        roadName: 'Western Express Highway',
        directionText: 'Southbound (towards Airport / Bandra)',
        speedLimitKph: 50,
        status: 'VERIFIED',
        lastVerifiedDate: '2026-08-10',
        sourceCategory: 'OFFICIAL_AUTHORITY',
        confirmationCount: 42,
      ),
    );
  }
}
