import 'package:flutter/material.dart';
import 'alert_card.dart';

class SignalEnforcementCard extends StatelessWidget {
  final String distanceText;

  const SignalEnforcementCard({
    Key? key,
    required this.distanceText,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return DriveGuardAlertCard(
      severity: AlertSeverity.p1,
      icon: Icons.traffic,
      title: 'Signal enforcement',
      subtitle: 'Camera at intersection',
      distanceText: distanceText,
    );
  }
}
