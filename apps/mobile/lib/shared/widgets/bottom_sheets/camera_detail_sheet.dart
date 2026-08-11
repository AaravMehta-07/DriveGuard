import 'package:flutter/material.dart';
import '../../../core/theme/tokens.dart';

class CameraDetailBottomSheet extends StatelessWidget {
  final String type;
  final String roadName;
  final String direction;
  final int? speedLimit;
  final String verificationStatus;
  final String lastVerifiedDate;
  final String sourceCategory;
  final int confirmationCount;

  const CameraDetailBottomSheet({
    Key? key,
    required this.type,
    required this.roadName,
    required this.direction,
    this.speedLimit,
    required this.verificationStatus,
    required this.lastVerifiedDate,
    required this.sourceCategory,
    required this.confirmationCount,
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
            children: [
              Icon(Icons.camera_alt, color: DriveGuardColors.primary, size: 32),
              const SizedBox(width: DriveGuardSpacing.sm),
              Expanded(
                child: Text(
                  '\$type Camera',
                  style: DriveGuardTypography.headlineMedium.copyWith(fontWeight: FontWeight.bold),
                ),
              ),
              if (speedLimit != null)
                Container(
                  padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 8),
                  decoration: BoxDecoration(
                    border: Border.all(color: DriveGuardColors.p0, width: 2),
                    shape: BoxShape.circle,
                  ),
                  child: Text(
                    speedLimit.toString(),
                    style: DriveGuardTypography.titleLarge.copyWith(fontWeight: FontWeight.bold),
                  ),
                ),
            ],
          ),
          const SizedBox(height: DriveGuardSpacing.md),
          Text(
            '\$roadName (\$direction)',
            style: DriveGuardTypography.bodyLarge,
          ),
          const Divider(height: 32),
          _buildInfoRow('Status', verificationStatus),
          _buildInfoRow('Last Verified', lastVerifiedDate),
          _buildInfoRow('Source', sourceCategory),
          _buildInfoRow('Confirmations', confirmationCount.toString()),
          const SizedBox(height: DriveGuardSpacing.lg),
        ],
      ),
    );
  }

  Widget _buildInfoRow(String label, String value) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 4.0),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        children: [
          Text(label, style: const TextStyle(color: Colors.grey)),
          Text(value, style: const TextStyle(fontWeight: FontWeight.w600)),
        ],
      ),
    );
  }
}
