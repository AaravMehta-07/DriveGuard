import 'package:flutter/material.dart';
import '../../core/theme/tokens.dart';

class DriveGuardSearchBar extends StatelessWidget {
  final VoidCallback onTap;
  final VoidCallback? onMicTap;

  const DriveGuardSearchBar({
    Key? key,
    required this.onTap,
    this.onMicTap,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Semantics(
      label: 'Search for a destination',
      button: true,
      child: GestureDetector(
        onTap: onTap,
        child: Container(
          height: 56,
          decoration: BoxDecoration(
            color: Theme.of(context).cardColor,
            borderRadius: BorderRadius.circular(28),
            boxShadow: [
              BoxShadow(
                color: Colors.black.withOpacity(0.15),
                blurRadius: 8,
                offset: const Offset(0, 4),
              ),
            ],
          ),
          padding: const EdgeInsets.symmetric(horizontal: DriveGuardSpacing.md),
          child: Row(
            children: [
              const Icon(Icons.search, size: 24),
              const SizedBox(width: DriveGuardSpacing.sm),
              Expanded(
                child: Text(
                  'Where to?',
                  style: DriveGuardTypography.bodyLarge.copyWith(
                    color: Theme.of(context).hintColor,
                  ),
                ),
              ),
              if (onMicTap != null)
                Semantics(
                  label: 'Voice search',
                  button: true,
                  child: IconButton(
                    icon: const Icon(Icons.mic, size: 24),
                    onPressed: onMicTap,
                    constraints: const BoxConstraints(
                      minWidth: 48,
                      minHeight: 48,
                    ),
                  ),
                ),
            ],
          ),
        ),
      ),
    );
  }
}
