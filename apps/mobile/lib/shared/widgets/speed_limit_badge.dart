import 'package:flutter/material.dart';
import '../../core/theme/tokens.dart';

class SpeedLimitBadge extends StatelessWidget {
  final int? speedLimit;

  const SpeedLimitBadge({
    Key? key,
    this.speedLimit,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    final displayValue = speedLimit?.toString() ?? '--';

    return Semantics(
      label: 'Speed limit \${speedLimit ?? 'unknown'}',
      child: Container(
        width: 64,
        height: 64,
        decoration: BoxDecoration(
          color: Colors.white,
          shape: BoxShape.circle,
          border: Border.all(
            color: DriveGuardColors.p0,
            width: 4,
          ),
          boxShadow: [
            BoxShadow(
              color: Colors.black.withOpacity(0.15),
              blurRadius: 4,
              offset: const Offset(0, 2),
            )
          ],
        ),
        alignment: Alignment.center,
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Text(
              'LIMIT',
              style: DriveGuardTypography.labelSmall.copyWith(
                color: Colors.black87,
                fontSize: 8,
                fontWeight: FontWeight.bold,
              ),
            ),
            Text(
              displayValue,
              style: const TextStyle(
                color: Colors.black,
                fontSize: 24,
                fontWeight: FontWeight.bold,
                fontFeatures: [FontFeature.tabularFigures()],
                height: 1.1,
              ),
            ),
          ],
        ),
      ),
    );
  }
}
