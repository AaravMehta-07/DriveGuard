import 'package:flutter/material.dart';
import '../../../core/theme/tokens.dart';
import '../route_event_row.dart';

class UpcomingEventsSheet extends StatelessWidget {
  const UpcomingEventsSheet({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.symmetric(vertical: DriveGuardSpacing.md),
      decoration: BoxDecoration(
        color: Theme.of(context).bottomSheetTheme.backgroundColor ?? Theme.of(context).cardColor,
        borderRadius: const BorderRadius.vertical(top: Radius.circular(24)),
      ),
      child: Column(
        mainAxisSize: MainAxisSize.min,
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Padding(
            padding: const EdgeInsets.symmetric(horizontal: DriveGuardSpacing.md),
            child: Text(
              'Upcoming on route',
              style: DriveGuardTypography.headlineMedium.copyWith(fontWeight: FontWeight.bold),
            ),
          ),
          const SizedBox(height: DriveGuardSpacing.sm),
          Expanded(
            child: ListView(
              shrinkWrap: true,
              children: [
                RouteEventRow(
                  icon: Icons.speed,
                  distanceText: '1.2 km',
                  title: 'Speed Camera',
                  subtitle: 'Limit 60 km/h',
                  onTap: () {},
                ),
                RouteEventRow(
                  icon: Icons.traffic,
                  distanceText: '3.5 km',
                  title: 'Signal Enforcement',
                  onTap: () {},
                ),
                RouteEventRow(
                  icon: Icons.not_interested,
                  distanceText: '5.0 km',
                  title: 'No Left Turn',
                  subtitle: 'Restricted 8AM - 8PM',
                  onTap: () {},
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }
}
