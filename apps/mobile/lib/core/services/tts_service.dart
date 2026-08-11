import 'package:flutter_tts/flutter_tts.dart';
import 'package:flutter/services.dart';

enum TtsVoiceMode { fullGuidance, alertsOnly, muted }

class TtsService {
  final FlutterTts _flutterTts = FlutterTts();
  TtsVoiceMode currentMode = TtsVoiceMode.fullGuidance;
  static const platform = MethodChannel('com.driveguard.app/native');

  TtsService() {
    _initTts();
  }

  void _initTts() async {
    await _flutterTts.setLanguage("en-US");
    await _flutterTts.setSpeechRate(0.5);
    await _flutterTts.setVolume(1.0);
    await _flutterTts.setPitch(1.0);
  }

  Future<void> speak(String text, int priority) async {
    if (currentMode == TtsVoiceMode.muted) return;
    
    // Attempt to request audio focus from native
    try {
      await platform.invokeMethod('requestAudioFocus');
    } catch (e) {
      // Audio focus request failed or not implemented
    }

    await _flutterTts.speak(text);
  }

  Future<void> stop() async {
    await _flutterTts.stop();
  }
}
