import 'package:flutter/material.dart';
import '../../core/theme/tokens.dart';
import '../../core/theme/typography.dart';

/// Legal & Attributions Screen for DriveGuard V3.
/// Displays required provider attributions, data limitation disclaimers,
/// OpenStreetMap ODbL acknowledgements, and open-source licenses.
class LegalScreen extends StatelessWidget {
  const LegalScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: DriveGuardColors.nightBackground,
      appBar: AppBar(
        backgroundColor: DriveGuardColors.nightSurface,
        title: const Text('Legal & Attributions', style: TextStyle(color: Colors.white, fontWeight: FontWeight.bold)),
        leading: IconButton(
          icon: const Icon(Icons.arrow_back_rounded, color: Colors.white),
          onPressed: () => Navigator.pop(context),
        ),
      ),
      body: ListView(
        padding: const EdgeInsets.all(16.0),
        children: [
          // Primary Legal & Safety Disclaimer
          Container(
            padding: const EdgeInsets.all(16),
            decoration: BoxDecoration(
              color: DriveGuardColors.warningAmber.withOpacity(0.1),
              borderRadius: BorderRadius.circular(DriveGuardRadii.medium),
              border: Border.all(color: DriveGuardColors.warningAmber.withOpacity(0.3)),
            ),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Row(
                  children: [
                    const Icon(Icons.gavel_rounded, color: DriveGuardColors.warningAmber, size: 24),
                    const SizedBox(width: 8),
                    Text('Data Limitation Disclaimer', style: DriveGuardTypography.body.copyWith(color: Colors.white, fontWeight: FontWeight.bold)),
                  ],
                ),
                const SizedBox(height: 8),
                Text(
                  'DriveGuard provides navigation and road-compliance assistance using available data. '
                  'Road conditions and restrictions can change. Always follow posted traffic signs, signals, '
                  'and directions from authorities. DriveGuard does not guarantee freedom from challans or penalties.',
                  style: DriveGuardTypography.secondaryMeta.copyWith(color: Colors.white70, height: 1.5),
                ),
              ],
            ),
          ),
          const SizedBox(height: 24),

          // Map & Data Attributions
          _buildHeader('MAP & DATA PROVIDER ATTRIBUTIONS'),
          _buildAttributionTile(
            title: 'Map Data & Basemaps',
            attribution: '© OpenStreetMap contributors, ODbL 1.0 / Mappls / Google Maps Platform',
            details: 'Map rendering and routing geometries provided by licensed basemap providers and OpenStreetMap under Open Database License.',
          ),
          _buildAttributionTile(
            title: 'Mumbai Traffic Police & Local Authorities',
            attribution: 'Official public notifications & traffic police orders',
            details: 'Traffic restrictions, temporary road closures, and official public notices ingested from published traffic authority notifications.',
          ),
          const Divider(color: Colors.white10, height: 32),

          // Open Source Licenses
          _buildHeader('OPEN SOURCE SOFTWARE'),
          ListTile(
            title: const Text('Third-Party Licenses', style: TextStyle(color: Colors.white, fontWeight: FontWeight.w600)),
            subtitle: const Text('View licenses for open source Flutter & Dart packages', style: TextStyle(color: Colors.white54, fontSize: 12)),
            trailing: const Icon(Icons.chevron_right_rounded, color: Colors.white54),
            onTap: () => showLicensePage(
              context: context,
              applicationName: 'DriveGuard',
              applicationVersion: '3.0.0',
              applicationLegalese: '© 2026 DriveGuard. India-First Traffic Compliance Platform.',
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildHeader(String title) {
    return Padding(
      padding: const EdgeInsets.only(left: 4.0, bottom: 8.0),
      child: Text(
        title,
        style: DriveGuardTypography.tinyAnnotation.copyWith(color: Colors.white38, letterSpacing: 1.2),
      ),
    );
  }

  Widget _buildAttributionTile({required String title, required String attribution, required String details}) {
    return Card(
      color: DriveGuardColors.nightSurface,
      margin: const EdgeInsets.only(bottom: 12.0),
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(DriveGuardRadii.medium)),
      child: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(title, style: DriveGuardTypography.body.copyWith(color: Colors.white, fontWeight: FontWeight.bold)),
            const SizedBox(height: 4),
            Text(attribution, style: DriveGuardTypography.secondaryMeta.copyWith(color: DriveGuardColors.brandPrimary, fontWeight: FontWeight.w600)),
            const SizedBox(height: 8),
            Text(details, style: DriveGuardTypography.secondaryMeta.copyWith(color: DriveGuardColors.nightTextSecondary, height: 1.4)),
          ],
        ),
      ),
    );
  }
}
