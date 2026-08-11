import 'package:flutter/material.dart';
import '../../core/theme/tokens.dart';

enum SpeedWarningState { normal, mild, severe }

class CurrentSpeedDisplay extends StatelessWidget {
  final int currentSpeed;
  final SpeedWarningState warningState;

  const CurrentSpeedDisplay({
    Key? key,
    required this.currentSpeed,
    this.warningState = SpeedWarningState.normal,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    Color textColor;
    switch (warningState) {
      case SpeedWarningState.mild:
        textColor = DriveGuardColors.p1;
        break;
      case SpeedWarningState.severe:
        textColor = DriveGuardColors.p0;
        break;
      case SpeedWarningState.normal:
      default:
        textColor = Theme.of(context).textTheme.headlineLarge!.color!;
        break;
    }

    return Semantics(
      label: 'Current speed \$currentSpeed kilometers per hour',
      child: Container(
        padding: const EdgeInsets.symmetric(
          horizontal: DriveGuardSpacing.md,
          vertical: DriveGuardSpacing.sm,
        ),
        decoration: BoxDecoration(
          color: Theme.of(context).cardColor.withOpacity(0.9),
          borderRadius: BorderRadius.circular(16),
          boxShadow: [
            BoxShadow(
              color: Colors.black.withOpacity(0.15),
              blurRadius: 8,
              offset: const Offset(0, 4),
            )
          ],
        ),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            AnimatedDefaultTextStyle(
              duration: const Duration(milliseconds: 200),
              style: TextStyle(
                color: textColor,
                fontSize: 32,
                fontWeight: FontWeight.bold,
                fontFeatures: const [FontFeature.tabularFigures()],
              ),
              child: Text(currentSpeed.toString()),
            ),
            Text(
              'km/h',
              style: DriveGuardTypography.labelMedium.copyWith(
                color: Theme.of(context).hintColor,
              ),
            ),
          ],
        ),
      ),
    );
  }
}
