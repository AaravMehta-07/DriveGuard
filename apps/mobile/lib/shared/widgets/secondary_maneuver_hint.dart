import 'package:flutter/material.dart';
import '../../core/theme/tokens.dart';

class SecondaryManeuverHint extends StatelessWidget {
  final IconData maneuverIcon;
  final String hintText;

  const SecondaryManeuverHint({
    Key? key,
    required this.maneuverIcon,
    required this.hintText,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Semantics(
      label: hintText,
      child: Container(
        margin: const EdgeInsets.symmetric(horizontal: DriveGuardSpacing.md),
        padding: const EdgeInsets.symmetric(
          horizontal: DriveGuardSpacing.md,
          vertical: DriveGuardSpacing.sm,
        ),
        decoration: BoxDecoration(
          color: Theme.of(context).cardColor.withOpacity(0.9),
          borderRadius: BorderRadius.circular(12),
          boxShadow: [
            BoxShadow(
              color: Colors.black.withOpacity(0.1),
              blurRadius: 4,
              offset: const Offset(0, 2),
            )
          ],
        ),
        child: Row(
          mainAxisSize: MainAxisSize.min,
          children: [
            Icon(
              maneuverIcon,
              size: 20,
              color: Theme.of(context).iconTheme.color,
            ),
            const SizedBox(width: DriveGuardSpacing.sm),
            Text(
              hintText,
              style: DriveGuardTypography.bodyMedium.copyWith(
                fontWeight: FontWeight.w600,
              ),
            ),
          ],
        ),
      ),
    );
  }
}
