import 'package:flutter/material.dart';
import '../../core/theme/tokens.dart';

class ETAFooter extends StatelessWidget {
  final String remainingTime;
  final String remainingDistance;
  final String arrivalTime;
  final VoidCallback? onTap;

  const ETAFooter({
    Key? key,
    required this.remainingTime,
    required this.remainingDistance,
    required this.arrivalTime,
    this.onTap,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Semantics(
      label: 'ETA \$arrivalTime, \$remainingTime, \$remainingDistance remaining',
      button: onTap != null,
      child: GestureDetector(
        onTap: onTap,
        child: Container(
          color: Theme.of(context).cardColor,
          padding: const EdgeInsets.all(DriveGuardSpacing.md),
          child: SafeArea(
            top: false,
            child: Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                Expanded(
                  child: Row(
                    children: [
                      Text(
                        remainingTime,
                        style: DriveGuardTypography.titleLarge.copyWith(
                          fontWeight: FontWeight.bold,
                          color: DriveGuardColors.primary,
                          fontFeatures: const [FontFeature.tabularFigures()],
                        ),
                      ),
                      const Padding(
                        padding: EdgeInsets.symmetric(horizontal: 8.0),
                        child: Text('•', style: TextStyle(color: Colors.grey)),
                      ),
                      Text(
                        remainingDistance,
                        style: DriveGuardTypography.titleMedium.copyWith(
                          fontFeatures: const [FontFeature.tabularFigures()],
                        ),
                      ),
                      const Padding(
                        padding: EdgeInsets.symmetric(horizontal: 8.0),
                        child: Text('•', style: TextStyle(color: Colors.grey)),
                      ),
                      Text(
                        arrivalTime,
                        style: DriveGuardTypography.titleMedium.copyWith(
                          fontFeatures: const [FontFeature.tabularFigures()],
                        ),
                      ),
                    ],
                  ),
                ),
                if (onTap != null)
                  const Icon(Icons.close, color: Colors.grey),
              ],
            ),
          ),
        ),
      ),
    );
  }
}
