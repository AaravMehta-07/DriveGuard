import 'package:flutter/material.dart';
import '../../core/theme/tokens.dart';

class PrimaryDriveButton extends StatelessWidget {
  final VoidCallback onPressed;
  final String label;
  final bool isCopilotMode;

  const PrimaryDriveButton({
    Key? key,
    required this.onPressed,
    this.label = 'START',
    this.isCopilotMode = false,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    final displayLabel = isCopilotMode ? 'Start DriveGuard' : label;

    return Semantics(
      label: 'Start navigation',
      button: true,
      child: ElevatedButton(
        onPressed: onPressed,
        style: ElevatedButton.styleFrom(
          backgroundColor: DriveGuardColors.primary,
          foregroundColor: Colors.white,
          minimumSize: const Size(double.infinity, 56),
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(28),
          ),
          elevation: 0,
        ),
        child: Text(
          displayLabel,
          style: DriveGuardTypography.titleLarge.copyWith(
            fontWeight: FontWeight.bold,
            color: Colors.white,
          ),
        ),
      ),
    );
  }
}
