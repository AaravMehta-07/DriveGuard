import 'package:flutter/material.dart';
import '../../../core/theme/tokens.dart';
import '../route_intelligence_summary.dart';
import '../primary_drive_button.dart';

class RouteSelectionBottomSheet extends StatelessWidget {
  final String routeLabel;
  final String travelTime;
  final String distance;
  final String arrivalTime;
  final VoidCallback onStartPressed;
  final VoidCallback onPreviewPressed;

  const RouteSelectionBottomSheet({
    Key? key,
    required this.routeLabel,
    required this.travelTime,
    required this.distance,
    required this.arrivalTime,
    required this.onStartPressed,
    required this.onPreviewPressed,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.all(DriveGuardSpacing.md),
      decoration: BoxDecoration(
        color: Theme.of(context).bottomSheetTheme.backgroundColor ?? Theme.of(context).cardColor,
        borderRadius: const BorderRadius.vertical(top: Radius.circular(24)),
      ),
      child: Column(
        mainAxisSize: MainAxisSize.min,
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              Text(
                travelTime,
                style: DriveGuardTypography.displaySmall.copyWith(
                  color: DriveGuardColors.primary,
                  fontWeight: FontWeight.bold,
                ),
              ),
              Text(
                routeLabel,
                style: DriveGuardTypography.titleMedium,
              ),
            ],
          ),
          const SizedBox(height: DriveGuardSpacing.xs),
          Text(
            '\$distance • ETA \$arrivalTime',
            style: DriveGuardTypography.bodyLarge,
          ),
          const SizedBox(height: DriveGuardSpacing.md),
          const RouteIntelligenceSummary(
            cameraCount: 3,
            signalCount: 1,
            restrictionCount: 2,
          ),
          const SizedBox(height: DriveGuardSpacing.lg),
          Row(
            children: [
              Expanded(
                child: PrimaryDriveButton(
                  onPressed: onStartPressed,
                ),
              ),
              const SizedBox(width: DriveGuardSpacing.md),
              OutlinedButton(
                onPressed: onPreviewPressed,
                style: OutlinedButton.styleFrom(
                  minimumSize: const Size(0, 56),
                  shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(28)),
                ),
                child: const Text('Preview'),
              ),
            ],
          ),
          const SizedBox(height: DriveGuardSpacing.lg),
        ],
      ),
    );
  }
}
