import 'package:flutter/material.dart';
import '../../core/theme/tokens.dart';

class MapFloatingButton extends StatelessWidget {
  final IconData icon;
  final VoidCallback onTap;
  final String semanticsLabel;
  final Color? backgroundColor;
  final Color? iconColor;

  const MapFloatingButton({
    Key? key,
    required this.icon,
    required this.onTap,
    required this.semanticsLabel,
    this.backgroundColor,
    this.iconColor,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Semantics(
      label: semanticsLabel,
      button: true,
      child: Material(
        color: backgroundColor ?? Theme.of(context).cardColor,
        shape: const CircleBorder(),
        elevation: 4,
        shadowColor: Colors.black.withOpacity(0.2),
        child: InkWell(
          onTap: onTap,
          customBorder: const CircleBorder(),
          child: Container(
            width: 48,
            height: 48,
            alignment: Alignment.center,
            child: Icon(
              icon,
              color: iconColor ?? Theme.of(context).iconTheme.color,
              size: 24,
            ),
          ),
        ),
      ),
    );
  }
}

class MapRecenterButton extends StatelessWidget {
  final VoidCallback onTap;

  const MapRecenterButton({Key? key, required this.onTap}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return MapFloatingButton(
      icon: Icons.my_location,
      onTap: onTap,
      semanticsLabel: 'Recenter map',
    );
  }
}

class MapOverviewButton extends StatelessWidget {
  final VoidCallback onTap;

  const MapOverviewButton({Key? key, required this.onTap}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return MapFloatingButton(
      icon: Icons.map_outlined,
      onTap: onTap,
      semanticsLabel: 'Map overview',
    );
  }
}

class MapMuteButton extends StatelessWidget {
  final VoidCallback onTap;
  final int muteState; // 0: full, 1: alerts-only, 2: muted

  const MapMuteButton({Key? key, required this.onTap, required this.muteState}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    IconData icon;
    String label;
    switch (muteState) {
      case 1:
        icon = Icons.campaign;
        label = 'Alerts only';
        break;
      case 2:
        icon = Icons.volume_off;
        label = 'Muted';
        break;
      case 0:
      default:
        icon = Icons.volume_up;
        label = 'Full volume';
        break;
    }
    return MapFloatingButton(
      icon: icon,
      onTap: onTap,
      semanticsLabel: 'Audio settings: \$label',
    );
  }
}

class MapReportButton extends StatelessWidget {
  final VoidCallback onTap;

  const MapReportButton({Key? key, required this.onTap}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return MapFloatingButton(
      icon: Icons.report_problem,
      onTap: onTap,
      semanticsLabel: 'Report an issue',
      backgroundColor: DriveGuardColors.primary,
      iconColor: Colors.white,
    );
  }
}

class MapLayersButton extends StatelessWidget {
  final VoidCallback onTap;

  const MapLayersButton({Key? key, required this.onTap}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return MapFloatingButton(
      icon: Icons.layers,
      onTap: onTap,
      semanticsLabel: 'Map layers',
    );
  }
}
