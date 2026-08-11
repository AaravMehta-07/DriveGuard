import 'package:flutter/material.dart';
import '../../core/theme/tokens.dart';

class ErrorBanner extends StatelessWidget {
  final String errorMessage;
  final String whatWorksMessage;
  final VoidCallback onDismiss;

  const ErrorBanner({
    Key? key,
    required this.errorMessage,
    required this.whatWorksMessage,
    required this.onDismiss,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Semantics(
      label: 'Error: \$errorMessage. \$whatWorksMessage',
      child: Container(
        margin: const EdgeInsets.all(DriveGuardSpacing.md),
        padding: const EdgeInsets.symmetric(
          horizontal: DriveGuardSpacing.md,
          vertical: DriveGuardSpacing.sm,
        ),
        decoration: BoxDecoration(
          color: DriveGuardColors.p0.withOpacity(0.95), // Red
          borderRadius: BorderRadius.circular(8),
          boxShadow: [
            BoxShadow(
              color: Colors.black.withOpacity(0.2),
              blurRadius: 4,
              offset: const Offset(0, 2),
            )
          ],
        ),
        child: Row(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Icon(Icons.error_outline, color: Colors.white, size: 24),
            const SizedBox(width: DriveGuardSpacing.sm),
            Expanded(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                mainAxisSize: MainAxisSize.min,
                children: [
                  Text(
                    errorMessage,
                    style: DriveGuardTypography.bodyLarge.copyWith(
                      color: Colors.white,
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                  Text(
                    whatWorksMessage,
                    style: DriveGuardTypography.bodyMedium.copyWith(
                      color: Colors.white.withOpacity(0.9),
                    ),
                  ),
                ],
              ),
            ),
            IconButton(
              icon: const Icon(Icons.close, color: Colors.white),
              onPressed: onDismiss,
              tooltip: 'Dismiss error',
            ),
          ],
        ),
      ),
    );
  }
}
