import 'package:flutter/material.dart';
import '../../core/theme/tokens.dart';

class LaneInfo {
  final IconData icon;
  final bool isHighlighted;

  const LaneInfo({required this.icon, required this.isHighlighted});
}

class LaneGuidancePanel extends StatelessWidget {
  final List<LaneInfo> lanes;

  const LaneGuidancePanel({
    Key? key,
    required this.lanes,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Semantics(
      label: 'Lane guidance showing \${lanes.length} lanes',
      child: Container(
        padding: const EdgeInsets.symmetric(
          horizontal: DriveGuardSpacing.md,
          vertical: DriveGuardSpacing.sm,
        ),
        decoration: BoxDecoration(
          color: Theme.of(context).colorScheme.surfaceVariant,
          borderRadius: BorderRadius.circular(12),
        ),
        child: Row(
          mainAxisSize: MainAxisSize.min,
          children: lanes.map((lane) {
            return Padding(
              padding: const EdgeInsets.symmetric(horizontal: 4.0),
              child: Icon(
                lane.icon,
                color: lane.isHighlighted
                    ? DriveGuardColors.primary
                    : Theme.of(context).disabledColor,
                size: 24,
              ),
            );
          }).toList(),
        ),
      ),
    );
  }
}
