import 'package:flutter/material.dart';
import '../../core/theme/tokens.dart';

class ClusterMarkerWidget extends StatelessWidget {
  final int count;
  final VoidCallback onTap;

  const ClusterMarkerWidget({
    Key? key,
    required this.count,
    required this.onTap,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Semantics(
      label: 'Cluster of $count items, tap to zoom',
      button: true,
      child: GestureDetector(
        onTap: onTap,
        child: Container(
          width: 48, // Touch target
          height: 48,
          alignment: Alignment.center,
          child: Container(
            width: 36,
            height: 36,
            decoration: BoxDecoration(
              color: DriveGuardColors.primary,
              shape: BoxShape.circle,
              border: Border.all(color: Colors.white, width: 2),
              boxShadow: [
                BoxShadow(
                  color: Colors.black.withOpacity(0.3),
                  blurRadius: 4,
                )
              ],
            ),
            alignment: Alignment.center,
            child: Text(
              count > 99 ? '99+' : count.toString(),
              style: DriveGuardTypography.labelLarge.copyWith(
                color: Colors.white,
                fontWeight: FontWeight.bold,
              ),
            ),
          ),
        ),
      ),
    );
  }
}
