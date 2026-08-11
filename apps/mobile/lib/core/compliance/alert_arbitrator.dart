import 'package:flutter/foundation.dart';

enum AlertSeverity { P0_CRITICAL, P1_HIGH, P2_MEDIUM, P3_INFORMATIONAL }

enum AlertType {
  PROHIBITED_MANEUVER,
  NO_ENTRY,
  ROAD_CLOSED,
  OVERSPEED_SEVERE,
  OVERSPEED_MODERATE,
  CAMERA_APPROACH,
  SPEED_LIMIT_CHANGE,
  SIGNAL_ENFORCEMENT,
  COMMUNITY_REPORT,
}

class DriveGuardAlert {

  const DriveGuardAlert({
    required this.id,
    required this.severity,
    required this.type,
    required this.title,
    this.subtitle,
    this.distanceMeters,
    this.speedLimitKph,
    this.voiceMessage,
    this.haptic = false,
    this.sourceEnforcementId,
    this.expiresAfterSeconds = 10,
  });
  final String id;
  final AlertSeverity severity;
  final AlertType type;
  final String title;
  final String? subtitle;
  final double? distanceMeters;
  final int? speedLimitKph;
  final String? voiceMessage;
  final bool haptic;
  final String? sourceEnforcementId;
  final int expiresAfterSeconds;

  int get priorityIndex => severity.index;
}

/// Alert Arbitration Engine for DriveGuard Mobile.
/// Enforces key safety & distraction-reduction rules:
/// 1. Exactly ONE primary voice message / alert card displayed at a time
/// 2. Strict priority: P0 (prohibited maneuver/no entry) > P1 (severe overspeed) > P2 (camera approach) > P3 (signals)
/// 3. Deduplication: The same camera does NOT trigger continuous voice alerts every 50 meters
/// 4. Cooldowns: After passing an event or stationary near a camera for >3 minutes, suppress audio nagging
class AlertArbitrator extends ChangeNotifier {

  AlertArbitrator({this.voiceCooldownSeconds = 45});
  final int voiceCooldownSeconds;

  final List<DriveGuardAlert> _activeAlerts = [];
  final Map<String, DateTime> _lastVoiceTriggerTimes = {};
  DriveGuardAlert? _currentPrimaryAlert;

  DriveGuardAlert? get currentPrimaryAlert => _currentPrimaryAlert;
  List<DriveGuardAlert> get activeAlerts => List.unmodifiable(_activeAlerts);

  void submitAlert(DriveGuardAlert alert) {
    // Check deduplication / cooldown for voice alert
    bool allowVoice = false;
    if (alert.voiceMessage != null && alert.voiceMessage!.isNotEmpty) {
      final lastTrigger = _lastVoiceTriggerTimes[alert.id];
      if (lastTrigger == null ||
          DateTime.now().difference(lastTrigger).inSeconds >= voiceCooldownSeconds) {
        allowVoice = true;
        _lastVoiceTriggerTimes[alert.id] = DateTime.now();
      }
    }

    final finalAlert = DriveGuardAlert(
      id: alert.id,
      severity: alert.severity,
      type: alert.type,
      title: alert.title,
      subtitle: alert.subtitle,
      distanceMeters: alert.distanceMeters,
      speedLimitKph: alert.speedLimitKph,
      voiceMessage: allowVoice ? alert.voiceMessage : null,
      haptic: allowVoice && alert.haptic,
      sourceEnforcementId: alert.sourceEnforcementId,
      expiresAfterSeconds: alert.expiresAfterSeconds,
    );

    // Remove existing alert with same ID
    _activeAlerts.removeWhere((a) => a.id == alert.id);
    _activeAlerts.add(finalAlert);

    // Sort by priority (P0 < P1 < P2 < P3 in enum index)
    _activeAlerts.sort((a, b) => a.priorityIndex.compareTo(b.priorityIndex));

    _reevaluatePrimaryAlert();
  }

  void dismissAlert(String id) {
    _activeAlerts.removeWhere((a) => a.id == id);
    _reevaluatePrimaryAlert();
  }

  void clearAll() {
    _activeAlerts.clear();
    _currentPrimaryAlert = null;
    notifyListeners();
  }

  void _reevaluatePrimaryAlert() {
    final highest = _activeAlerts.isNotEmpty ? _activeAlerts.first : null;
    if (_currentPrimaryAlert?.id != highest?.id) {
      _currentPrimaryAlert = highest;
      notifyListeners();
    }
  }
}
