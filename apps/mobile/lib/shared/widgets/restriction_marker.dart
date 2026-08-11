import 'package:flutter/material.dart';
import '../../core/theme/tokens.dart';

enum RestrictionType { noLeft, noRight, noUTurn, noEntry }

class RestrictionMarkerIcon extends StatelessWidget {
  final RestrictionType type;

  const RestrictionMarkerIcon({
    Key? key,
    required this.type,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    IconData iconData;
    switch (type) {
      case RestrictionType.noLeft:
        iconData = Icons.turn_left; // Simplified for placeholder
        break;
      case RestrictionType.noRight:
        iconData = Icons.turn_right;
        break;
      case RestrictionType.noUTurn:
        iconData = Icons.u_turn_left;
        break;
      case RestrictionType.noEntry:
        iconData = Icons.do_not_disturb_on;
        break;
    }

    return Semantics(
      label: '\${type.name} restriction marker',
      child: Container(
        width: 48, // Expanded touch target
        height: 48,
        alignment: Alignment.center,
        child: Container(
          width: 32,
          height: 32,
          decoration: BoxDecoration(
            color: Colors.white,
            shape: BoxShape.circle,
            border: Border.all(color: DriveGuardColors.p0, width: 3), // Red prohibition style
            boxShadow: [
              BoxShadow(
                color: Colors.black.withOpacity(0.3),
                blurRadius: 4,
              )
            ],
          ),
          child: Stack(
            alignment: Alignment.center,
            children: [
              Icon(
                iconData,
                color: Colors.black87,
                size: 18,
              ),
              if (type != RestrictionType.noEntry)
                Transform.rotate(
                  angle: -0.785, // -45 degrees
                  child: Container(
                    width: 24,
                    height: 3,
                    color: DriveGuardColors.p0,
                  ),
                ),
            ],
          ),
        ),
      ),
    );
  }
}
