import 'package:flutter/material.dart';
import '../../core/theme/tokens.dart';

class CopilotActivePill extends StatelessWidget {
  const CopilotActivePill({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Semantics(
      label: 'DriveGuard Copilot mode active',
      child: Container(
        padding: const EdgeInsets.symmetric(
          horizontal: DriveGuardSpacing.md,
          vertical: DriveGuardSpacing.xs,
        ),
        decoration: BoxDecoration(
          color: DriveGuardColors.primary.withOpacity(0.9),
          borderRadius: BorderRadius.circular(16),
          boxShadow: [
            BoxShadow(
              color: Colors.black.withOpacity(0.15),
              blurRadius: 4,
              offset: const Offset(0, 2),
            )
          ],
        ),
        child: Row(
          mainAxisSize: MainAxisSize.min,
          children: [
            const Icon(Icons.shield, color: Colors.white, size: 16),
            const SizedBox(width: DriveGuardSpacing.sm),
            Text(
              'DriveGuard Active',
              style: DriveGuardTypography.labelMedium.copyWith(
                color: Colors.white,
                fontWeight: FontWeight.bold,
              ),
            ),
          ],
        ),
      ),
    );
  }
}
