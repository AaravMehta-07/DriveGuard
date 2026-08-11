import 'package:flutter/material.dart';
import 'alert_card.dart';

class RestrictionWarningCard extends StatelessWidget {
  final String restrictionText;
  final String distanceText;

  const RestrictionWarningCard({
    Key? key,
    required this.restrictionText,
    required this.distanceText,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return DriveGuardAlertCard(
      severity: AlertSeverity.p0,
      icon: Icons.not_interested,
      title: restrictionText,
      subtitle: 'Restricted movement',
      distanceText: distanceText,
    );
  }
}
