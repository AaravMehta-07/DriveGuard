import 'package:flutter/material.dart';
import '../../core/theme/tokens.dart';

enum EnforcementType { speedCamera, redLight, combined, averageSpeed, signalEnforcement }
enum VerificationStatus { verified, probable, reported }

class EnforcementMarkerIcon extends StatelessWidget {
  final EnforcementType type;
  final VerificationStatus status;

  const EnforcementMarkerIcon({
    Key? key,
    required this.type,
    required this.status,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    IconData iconData;
    switch (type) {
      case EnforcementType.speedCamera:
        iconData = Icons.speed;
        break;
      case EnforcementType.redLight:
        iconData = Icons.traffic;
        break;
      case EnforcementType.combined:
        iconData = Icons.camera_alt;
        break;
      case EnforcementType.averageSpeed:
        iconData = Icons.timelapse;
        break;
      case EnforcementType.signalEnforcement:
        iconData = Icons.security;
        break;
    }

    double opacity = 1.0;
    bool isDashed = false;

    if (status == VerificationStatus.probable) {
      opacity = 0.8;
    } else if (status == VerificationStatus.reported) {
      opacity = 0.6;
      isDashed = true;
    }

    return Semantics(
      label: '\${type.name} enforcement marker, status: \${status.name}',
      child: Container(
        width: 48, // Expanded hit-test area
        height: 48,
        alignment: Alignment.center,
        child: Container(
          width: 32,
          height: 32,
          decoration: BoxDecoration(
            color: DriveGuardColors.p0.withOpacity(opacity),
            shape: BoxShape.circle,
            border: isDashed
                ? Border.all(color: Colors.white, width: 2, style: BorderStyle.solid) // Simplification for dashed
                : Border.all(color: Colors.white, width: 2),
            boxShadow: [
              BoxShadow(
                color: Colors.black.withOpacity(0.3),
                blurRadius: 4,
              )
            ],
          ),
          child: Icon(
            iconData,
            color: Colors.white.withOpacity(opacity),
            size: 18,
          ),
        ),
      ),
    );
  }
}
