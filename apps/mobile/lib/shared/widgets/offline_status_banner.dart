import 'package:flutter/material.dart';
import '../../core/theme/tokens.dart';

class OfflineStatusBanner extends StatelessWidget {
  const OfflineStatusBanner({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Semantics(
      label: 'You are offline. Downloaded data still available.',
      child: Container(
        padding: const EdgeInsets.symmetric(
          horizontal: DriveGuardSpacing.md,
          vertical: DriveGuardSpacing.sm,
        ),
        color: DriveGuardColors.p3.withOpacity(0.9), // Blue-gray
        child: Row(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            const Icon(Icons.cloud_off, color: Colors.white, size: 16),
            const SizedBox(width: DriveGuardSpacing.sm),
            Text(
              "You're offline · Downloaded data still available",
              style: DriveGuardTypography.labelMedium.copyWith(
                color: Colors.white,
              ),
            ),
          ],
        ),
      ),
    );
  }
}
