import 'package:flutter/material.dart';
import '../../../core/theme/tokens.dart';

class ReportBottomSheet extends StatelessWidget {
  final VoidCallback onReportSubmitted;

  const ReportBottomSheet({Key? key, required this.onReportSubmitted}) : super(key: key);

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
        children: [
          Text(
            'Report an issue',
            style: DriveGuardTypography.headlineMedium.copyWith(fontWeight: FontWeight.bold),
          ),
          const SizedBox(height: DriveGuardSpacing.md),
          GridView.count(
            crossAxisCount: 3,
            shrinkWrap: true,
            physics: const NeverScrollableScrollPhysics(),
            mainAxisSpacing: 16,
            crossAxisSpacing: 16,
            children: [
              _buildReportButton(context, Icons.speed, 'Camera'),
              _buildReportButton(context, Icons.traffic, 'Signal camera'),
              _buildReportButton(context, Icons.not_interested, 'Restriction'),
              _buildReportButton(context, Icons.remove_road, 'Closure'),
              _buildReportButton(context, Icons.local_police, 'Police'),
              _buildReportButton(context, Icons.speed, 'Speed limit'),
              _buildReportButton(context, Icons.map, 'Map issue'),
            ],
          ),
          const SizedBox(height: DriveGuardSpacing.lg),
        ],
      ),
    );
  }

  Widget _buildReportButton(BuildContext context, IconData icon, String label) {
    return InkWell(
      onTap: () {
        // Handle selection and close
        onReportSubmitted();
        Navigator.pop(context);
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content: Text('Thanks for reporting!')),
        );
      },
      child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          Container(
            width: 64,
            height: 64,
            decoration: BoxDecoration(
              color: Theme.of(context).colorScheme.surfaceVariant,
              shape: BoxShape.circle,
            ),
            child: Icon(icon, size: 32, color: DriveGuardColors.primary),
          ),
          const SizedBox(height: 8),
          Text(
            label,
            textAlign: TextAlign.center,
            style: const TextStyle(fontWeight: FontWeight.w600, fontSize: 12),
          ),
        ],
      ),
    );
  }
}
