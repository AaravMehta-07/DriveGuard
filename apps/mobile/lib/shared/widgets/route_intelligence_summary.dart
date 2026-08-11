import 'package:flutter/material.dart';
import '../../core/theme/tokens.dart';

class RouteIntelligenceSummary extends StatelessWidget {
  final int cameraCount;
  final int signalCount;
  final int restrictionCount;
  final VoidCallback? onTap;

  const RouteIntelligenceSummary({
    Key? key,
    this.cameraCount = 0,
    this.signalCount = 0,
    this.restrictionCount = 0,
    this.onTap,
  }) : super(key: key);

  Widget _buildItem(BuildContext context, IconData icon, int count) {
    if (count == 0) return const SizedBox.shrink();
    return Padding(
      padding: const EdgeInsets.only(right: DriveGuardSpacing.sm),
      child: Row(
        mainAxisSize: MainAxisSize.min,
        children: [
          Icon(icon, size: 16, color: Theme.of(context).iconTheme.color),
          const SizedBox(width: 4),
          Text(
            count.toString(),
            style: DriveGuardTypography.labelMedium.copyWith(
              fontWeight: FontWeight.bold,
            ),
          ),
        ],
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Semantics(
      label: 'Route intelligence summary: \$cameraCount cameras, \$signalCount signals, \$restrictionCount restrictions',
      button: onTap != null,
      child: GestureDetector(
        onTap: onTap,
        child: Container(
          padding: const EdgeInsets.symmetric(
            horizontal: DriveGuardSpacing.md,
            vertical: DriveGuardSpacing.sm,
          ),
          decoration: BoxDecoration(
            color: Theme.of(context).colorScheme.surfaceVariant,
            borderRadius: BorderRadius.circular(8),
          ),
          child: Row(
            mainAxisSize: MainAxisSize.min,
            children: [
              _buildItem(context, Icons.speed, cameraCount),
              _buildItem(context, Icons.traffic, signalCount),
              _buildItem(context, Icons.not_interested, restrictionCount),
            ],
          ),
        ),
      ),
    );
  }
}
