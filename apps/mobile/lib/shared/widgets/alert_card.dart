import 'package:flutter/material.dart';
import '../../core/theme/tokens.dart';

enum AlertSeverity { p0, p1, p2, p3 }

class DriveGuardAlertCard extends StatelessWidget {
  final AlertSeverity severity;
  final IconData icon;
  final String title;
  final String subtitle;
  final String distanceText;

  const DriveGuardAlertCard({
    Key? key,
    required this.severity,
    required this.icon,
    required this.title,
    required this.subtitle,
    required this.distanceText,
  }) : super(key: key);

  Color _getSeverityColor() {
    switch (severity) {
      case AlertSeverity.p0:
        return DriveGuardColors.p0; // Red
      case AlertSeverity.p1:
        return DriveGuardColors.p1; // Orange
      case AlertSeverity.p2:
        return DriveGuardColors.p2; // Amber
      case AlertSeverity.p3:
        return DriveGuardColors.p3; // Blue-gray
    }
  }

  @override
  Widget build(BuildContext context) {
    final color = _getSeverityColor();

    return Semantics(
      label: 'Alert: \$title, \$subtitle, \$distanceText',
      child: Container(
        margin: const EdgeInsets.symmetric(horizontal: DriveGuardSpacing.md, vertical: DriveGuardSpacing.sm),
        decoration: BoxDecoration(
          color: Theme.of(context).cardColor,
          borderRadius: BorderRadius.circular(12),
          border: Border(left: BorderSide(color: color, width: 6)),
          boxShadow: [
            BoxShadow(
              color: Colors.black.withOpacity(0.15),
              blurRadius: 8,
              offset: const Offset(0, 4),
            )
          ],
        ),
        child: Padding(
          padding: const EdgeInsets.all(DriveGuardSpacing.md),
          child: Row(
            children: [
              Container(
                padding: const EdgeInsets.all(8),
                decoration: BoxDecoration(
                  color: color.withOpacity(0.1),
                  shape: BoxShape.circle,
                ),
                child: Icon(icon, color: color, size: 28),
              ),
              const SizedBox(width: DriveGuardSpacing.md),
              Expanded(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  mainAxisSize: MainAxisSize.min,
                  children: [
                    Text(
                      title,
                      style: DriveGuardTypography.titleMedium.copyWith(fontWeight: FontWeight.bold),
                    ),
                    Text(
                      subtitle,
                      style: DriveGuardTypography.bodyMedium,
                    ),
                  ],
                ),
              ),
              Text(
                distanceText,
                style: DriveGuardTypography.titleMedium.copyWith(
                  fontWeight: FontWeight.bold,
                  fontFeatures: const [FontFeature.tabularFigures()],
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
