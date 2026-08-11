import 'package:flutter/material.dart';
import '../../core/theme/tokens.dart';

class PermissionExplanationSheet extends StatelessWidget {
  final IconData icon;
  final String title;
  final String explanation;
  final bool isRequired;
  final VoidCallback onGrantPressed;

  const PermissionExplanationSheet({
    Key? key,
    required this.icon,
    required this.title,
    required this.explanation,
    this.isRequired = true,
    required this.onGrantPressed,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.all(DriveGuardSpacing.lg),
      decoration: BoxDecoration(
        color: Theme.of(context).bottomSheetTheme.backgroundColor ?? Theme.of(context).cardColor,
        borderRadius: const BorderRadius.vertical(top: Radius.circular(24)),
      ),
      child: Column(
        mainAxisSize: MainAxisSize.min,
        children: [
          Container(
            width: 80,
            height: 80,
            decoration: BoxDecoration(
              color: DriveGuardColors.primary.withOpacity(0.1),
              shape: BoxShape.circle,
            ),
            child: Icon(icon, size: 40, color: DriveGuardColors.primary),
          ),
          const SizedBox(height: DriveGuardSpacing.lg),
          Row(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              Text(
                title,
                style: DriveGuardTypography.headlineMedium.copyWith(fontWeight: FontWeight.bold),
                textAlign: TextAlign.center,
              ),
              if (!isRequired) ...[
                const SizedBox(width: 8),
                Container(
                  padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
                  decoration: BoxDecoration(
                    color: Theme.of(context).disabledColor.withOpacity(0.2),
                    borderRadius: BorderRadius.circular(12),
                  ),
                  child: Text(
                    'Optional',
                    style: DriveGuardTypography.labelSmall.copyWith(
                      color: Theme.of(context).hintColor,
                    ),
                  ),
                ),
              ],
            ],
          ),
          const SizedBox(height: DriveGuardSpacing.md),
          Text(
            explanation,
            style: DriveGuardTypography.bodyLarge,
            textAlign: TextAlign.center,
          ),
          const SizedBox(height: DriveGuardSpacing.xl),
          ElevatedButton(
            onPressed: onGrantPressed,
            style: ElevatedButton.styleFrom(
              backgroundColor: DriveGuardColors.primary,
              foregroundColor: Colors.white,
              minimumSize: const Size(double.infinity, 56),
              shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(28)),
            ),
            child: const Text('Grant Permission', style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
          ),
          if (!isRequired) ...[
            const SizedBox(height: DriveGuardSpacing.md),
            TextButton(
              onPressed: () => Navigator.pop(context),
              child: Text(
                'Not Now',
                style: TextStyle(color: Theme.of(context).hintColor),
              ),
            ),
          ],
          const SizedBox(height: DriveGuardSpacing.lg),
        ],
      ),
    );
  }
}
