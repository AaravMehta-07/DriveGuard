import 'package:flutter/material.dart';
import '../../../core/theme/tokens.dart';

class DestinationBottomSheet extends StatelessWidget {
  final String placeName;
  final String address;
  final String travelTime;
  final VoidCallback onDirectionsPressed;
  final VoidCallback onSavePressed;
  final VoidCallback onSharePressed;

  const DestinationBottomSheet({
    Key? key,
    required this.placeName,
    required this.address,
    required this.travelTime,
    required this.onDirectionsPressed,
    required this.onSavePressed,
    required this.onSharePressed,
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
          Text(
            placeName,
            style: DriveGuardTypography.headlineMedium.copyWith(fontWeight: FontWeight.bold),
          ),
          const SizedBox(height: DriveGuardSpacing.xs),
          Text(
            address,
            style: DriveGuardTypography.bodyMedium,
          ),
          const SizedBox(height: DriveGuardSpacing.sm),
          Text(
            travelTime,
            style: DriveGuardTypography.titleMedium.copyWith(
              color: DriveGuardColors.primary,
              fontWeight: FontWeight.bold,
            ),
          ),
          const SizedBox(height: DriveGuardSpacing.lg),
          Row(
            children: [
              Expanded(
                child: ElevatedButton(
                  onPressed: onDirectionsPressed,
                  style: ElevatedButton.styleFrom(
                    backgroundColor: DriveGuardColors.primary,
                    minimumSize: const Size(0, 56),
                    shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(28)),
                  ),
                  child: Text('Directions', style: TextStyle(color: Colors.white, fontSize: 18)),
                ),
              ),
              const SizedBox(width: DriveGuardSpacing.md),
              IconButton(
                onPressed: onSavePressed,
                icon: const Icon(Icons.bookmark_border),
                tooltip: 'Save',
              ),
              IconButton(
                onPressed: onSharePressed,
                icon: const Icon(Icons.share),
                tooltip: 'Share',
              ),
            ],
          ),
          const SizedBox(height: DriveGuardSpacing.lg),
        ],
      ),
    );
  }
}
