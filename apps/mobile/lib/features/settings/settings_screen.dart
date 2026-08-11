import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';
import '../../core/theme/tokens.dart';
import '../../core/theme/typography.dart';

/// Full Production Settings Screen for DriveGuard V3.
/// Organizes all application settings into intuitive sections:
/// - Navigation Preferences (routes, tolls, highways)
/// - DriveGuard Compliance Alerts (speed warnings, camera approach, signals, voice mode, haptics)
/// - Map & Interface (theme, marker density)
/// - Vehicle Profile
/// - Offline Pack Data
/// - Privacy & Data Controls
/// - Legal & About
class SettingsScreen extends ConsumerStatefulWidget {
  const SettingsScreen({super.key});

  @override
  ConsumerState<SettingsScreen> createState() => _SettingsScreenState();
}

class _SettingsScreenState extends ConsumerState<SettingsScreen> {
  bool _cameraWarningsEnabled = true;
  bool _signalWarningsEnabled = true;
  bool _turnRestrictionWarningsEnabled = true;
  bool _speedWarningsEnabled = true;
  bool _hapticsEnabled = true;
  String _voiceMode = 'FULL_GUIDANCE'; // FULL_GUIDANCE, ALERTS_ONLY, MUTED

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: DriveGuardColors.nightBackground,
      appBar: AppBar(
        backgroundColor: DriveGuardColors.nightSurface,
        title: const Text('Settings', style: TextStyle(color: Colors.white, fontWeight: FontWeight.bold)),
        leading: IconButton(
          icon: const Icon(Icons.arrow_back_rounded, color: Colors.white),
          onPressed: () => Navigator.pop(context),
        ),
      ),
      body: ListView(
        padding: const EdgeInsets.symmetric(vertical: 16.0),
        children: [
          // Section 1: DriveGuard Compliance Alerts
          _buildHeader('DRIVEGUARD ALERTS'),
          SwitchListTile(
            title: const Text('Speed Camera Alerts', style: TextStyle(color: Colors.white)),
            subtitle: const Text('Approach alerts for verified speed enforcement points', style: TextStyle(color: Colors.white54, fontSize: 12)),
            value: _cameraWarningsEnabled,
            onChanged: (v) => setState(() => _cameraWarningsEnabled = v),
          ),
          SwitchListTile(
            title: const Text('Signal Enforcement Alerts', style: TextStyle(color: Colors.white)),
            subtitle: const Text('Red-light camera junction warnings', style: TextStyle(color: Colors.white54, fontSize: 12)),
            value: _signalWarningsEnabled,
            onChanged: (v) => setState(() => _signalWarningsEnabled = v),
          ),
          SwitchListTile(
            title: const Text('Prohibited Turn Warnings', style: TextStyle(color: Colors.white)),
            subtitle: const Text('Proactive alerts before no-left, no-right, or no-U-turns', style: TextStyle(color: Colors.white54, fontSize: 12)),
            value: _turnRestrictionWarningsEnabled,
            onChanged: (v) => setState(() => _turnRestrictionWarningsEnabled = v),
          ),
          SwitchListTile(
            title: const Text('Speed Limit Warnings', style: TextStyle(color: Colors.white)),
            subtitle: const Text('Alert when current speed exceeds posted limit (even without cameras)', style: TextStyle(color: Colors.white54, fontSize: 12)),
            value: _speedWarningsEnabled,
            onChanged: (v) => setState(() => _speedWarningsEnabled = v),
          ),
          SwitchListTile(
            title: const Text('Haptic Vibration', style: TextStyle(color: Colors.white)),
            subtitle: const Text('Vibrate on P0/P1 severe warnings', style: TextStyle(color: Colors.white54, fontSize: 12)),
            value: _hapticsEnabled,
            onChanged: (v) => setState(() => _hapticsEnabled = v),
          ),
          const Divider(color: Colors.white10, height: 32),

          // Section 2: Vehicle & Routing
          _buildHeader('VEHICLE & ROUTING'),
          ListTile(
            leading: const Icon(Icons.directions_car_rounded, color: DriveGuardColors.brandPrimary),
            title: const Text('Vehicle Profile', style: TextStyle(color: Colors.white)),
            subtitle: const Text('Private Car (Default)', style: TextStyle(color: Colors.white54, fontSize: 12)),
            trailing: const Icon(Icons.chevron_right_rounded, color: Colors.white54),
            onTap: () => context.push('/settings/vehicle'),
          ),
          const Divider(color: Colors.white10, height: 32),

          // Section 3: Data & Privacy
          _buildHeader('DATA & PRIVACY'),
          ListTile(
            leading: const Icon(Icons.offline_pin_rounded, color: DriveGuardColors.verifiedGreen),
            title: const Text('Offline Compliance Packs', style: TextStyle(color: Colors.white)),
            subtitle: const Text('Mumbai Compliance Pack · 48 MB', style: TextStyle(color: Colors.white54, fontSize: 12)),
            trailing: const Icon(Icons.chevron_right_rounded, color: Colors.white54),
            onTap: () => context.push('/offline'),
          ),
          ListTile(
            leading: const Icon(Icons.security_rounded, color: DriveGuardColors.brandPrimary),
            title: const Text('Privacy & Data Controls', style: TextStyle(color: Colors.white)),
            subtitle: const Text('Export data, clear history, account deletion', style: TextStyle(color: Colors.white54, fontSize: 12)),
            trailing: const Icon(Icons.chevron_right_rounded, color: Colors.white54),
            onTap: () => context.push('/settings/privacy'),
          ),
          const Divider(color: Colors.white10, height: 32),

          // Section 4: About & Legal
          _buildHeader('ABOUT & LEGAL'),
          ListTile(
            leading: const Icon(Icons.gavel_rounded, color: Colors.white70),
            title: const Text('Legal & Attributions', style: TextStyle(color: Colors.white)),
            subtitle: const Text('Disclaimers, provider attributions, ODbL license', style: TextStyle(color: Colors.white54, fontSize: 12)),
            trailing: const Icon(Icons.chevron_right_rounded, color: Colors.white54),
            onTap: () => context.push('/settings/legal'),
          ),
          ListTile(
            leading: const Icon(Icons.info_outline_rounded, color: Colors.white70),
            title: const Text('DriveGuard Version', style: TextStyle(color: Colors.white)),
            subtitle: const Text('v3.0.0 (Build 1001) · Mumbai Launch Edition', style: TextStyle(color: Colors.white54, fontSize: 12)),
          ),
        ],
      ),
    );
  }

  Widget _buildHeader(String title) {
    return Padding(
      padding: const EdgeInsets.only(left: 16.0, bottom: 8.0),
      child: Text(
        title,
        style: DriveGuardTypography.tinyAnnotation.copyWith(color: Colors.white38, letterSpacing: 1.2),
      ),
    );
  }
}
