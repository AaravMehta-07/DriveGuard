import 'package:flutter/material.dart';
import '../../../core/theme/tokens.dart';

class LayersBottomSheet extends StatelessWidget {
  const LayersBottomSheet({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.all(DriveGuardSpacing.md),
      decoration: BoxDecoration(
        color: Theme.of(context).bottomSheetTheme.backgroundColor ?? Theme.of(context).cardColor,
        borderRadius: const BorderRadius.vertical(top: Radius.circular(24)),
      ),
      child: Column(
        mainAxisSize: MainAxisSize.min,
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(
            'Map Details',
            style: DriveGuardTypography.headlineMedium.copyWith(fontWeight: FontWeight.bold),
          ),
          const SizedBox(height: DriveGuardSpacing.md),
          _buildSectionTitle('Map'),
          SwitchListTile(title: const Text('Traffic'), value: true, onChanged: (v) {}),
          SwitchListTile(title: const Text('Satellite'), value: false, onChanged: (v) {}),
          const Divider(),
          _buildSectionTitle('DriveGuard'),
          SwitchListTile(title: const Text('Cameras'), value: true, onChanged: (v) {}),
          SwitchListTile(title: const Text('Signals'), value: true, onChanged: (v) {}),
          SwitchListTile(title: const Text('Restrictions'), value: true, onChanged: (v) {}),
          const Divider(),
          _buildSectionTitle('Optional'),
          SwitchListTile(title: const Text('Challan Hotspots'), value: false, onChanged: (v) {}),
          SwitchListTile(title: const Text('Parking'), value: false, onChanged: (v) {}),
          const SizedBox(height: DriveGuardSpacing.lg),
        ],
      ),
    );
  }

  Widget _buildSectionTitle(String title) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 8.0, horizontal: 16.0),
      child: Text(
        title.toUpperCase(),
        style: const TextStyle(
          color: Colors.grey,
          fontWeight: FontWeight.bold,
          letterSpacing: 1.2,
        ),
      ),
    );
  }
}
