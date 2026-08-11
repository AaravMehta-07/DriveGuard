import 'package:vibration/vibration.dart';

enum HapticLevel { light, medium, heavy }

class HapticService {
  Future<void> vibrate(HapticLevel level) async {
    bool? hasVibrator = await Vibration.hasVibrator();
    if (hasVibrator == true) {
      switch (level) {
        case HapticLevel.light:
          Vibration.vibrate(duration: 50);
          break;
        case HapticLevel.medium:
          Vibration.vibrate(duration: 150);
          break;
        case HapticLevel.heavy:
          Vibration.vibrate(duration: 500, amplitude: 255);
          break;
      }
    }
  }
}
