import 'package:flutter/material.dart';
import '../../core/theme/tokens.dart';

class NavigationManeuverCard extends StatelessWidget {
  final IconData maneuverIcon;
  final String distanceText;
  final String actionText;
  final String targetRoadName;

  const NavigationManeuverCard({
    Key? key,
    required this.maneuverIcon,
    required this.distanceText,
    required this.actionText,
    required this.targetRoadName,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Semantics(
      label: 'In \$distanceText, \$actionText \$targetRoadName',
      child: Container(
        margin: const EdgeInsets.all(DriveGuardSpacing.md),
        padding: const EdgeInsets.all(DriveGuardSpacing.md),
        decoration: BoxDecoration(
          color: Theme.of(context).cardColor.withOpacity(0.95),
          borderRadius: BorderRadius.circular(16),
          boxShadow: [
            BoxShadow(
              color: Colors.black.withOpacity(0.2),
              blurRadius: 10,
              offset: const Offset(0, 4),
            )
          ],
        ),
        child: Row(
          children: [
            Container(
              width: 64,
              height: 64,
              decoration: BoxDecoration(
                color: DriveGuardColors.primary.withOpacity(0.1),
                borderRadius: BorderRadius.circular(12),
              ),
              child: Icon(
                maneuverIcon,
                size: 40,
                color: DriveGuardColors.primary,
              ),
            ),
            const SizedBox(width: DriveGuardSpacing.md),
            Expanded(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                mainAxisSize: MainAxisSize.min,
                children: [
                  Text(
                    distanceText,
                    style: DriveGuardTypography.headlineLarge.copyWith(
                      fontWeight: FontWeight.bold,
                      fontFeatures: const [FontFeature.tabularFigures()],
                    ),
                  ),
                  Text(
                    actionText,
                    style: DriveGuardTypography.bodyMedium,
                  ),
                  Text(
                    targetRoadName,
                    style: DriveGuardTypography.titleMedium.copyWith(
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }
}
