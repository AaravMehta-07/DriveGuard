import 'package:flutter/material.dart';
import 'alert_card.dart';

class CameraApproachCard extends StatelessWidget {
  final String distanceText;
  final String speedLimit;

  const CameraApproachCard({
    Key? key,
    required this.distanceText,
    required this.speedLimit,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return DriveGuardAlertCard(
      severity: AlertSeverity.p1,
      icon: Icons.speed,
      title: 'Speed camera',
      subtitle: 'Limit \$speedLimit km/h',
      distanceText: distanceText,
    );
  }
}
