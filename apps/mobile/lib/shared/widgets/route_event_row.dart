import 'package:flutter/material.dart';
import '../../core/theme/tokens.dart';

class RouteEventRow extends StatelessWidget {
  final IconData icon;
  final String distanceText;
  final String title;
  final String? subtitle;
  final VoidCallback? onTap;

  const RouteEventRow({
    Key? key,
    required this.icon,
    required this.distanceText,
    required this.title,
    this.subtitle,
    this.onTap,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Semantics(
      label: 'Event: \$title in \$distanceText',
      button: onTap != null,
      child: InkWell(
        onTap: onTap,
        child: Padding(
          padding: const EdgeInsets.symmetric(
            horizontal: DriveGuardSpacing.md,
            vertical: DriveGuardSpacing.sm,
          ),
          child: Row(
            children: [
              Container(
                width: 40,
                height: 40,
                decoration: BoxDecoration(
                  color: Theme.of(context).colorScheme.surfaceVariant,
                  shape: BoxShape.circle,
                ),
                child: Icon(icon, size: 20),
              ),
              const SizedBox(width: DriveGuardSpacing.md),
              Expanded(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      title,
                      style: DriveGuardTypography.bodyLarge.copyWith(
                        fontWeight: FontWeight.w600,
                      ),
                    ),
                    if (subtitle != null)
                      Text(
                        subtitle!,
                        style: DriveGuardTypography.bodyMedium.copyWith(
                          color: Theme.of(context).hintColor,
                        ),
                      ),
                  ],
                ),
              ),
              Text(
                distanceText,
                style: DriveGuardTypography.bodyMedium.copyWith(
                  fontWeight: FontWeight.bold,
                  fontFeatures: const [FontFeature.tabularFigures()],
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
