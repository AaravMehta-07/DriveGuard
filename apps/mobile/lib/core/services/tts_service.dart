enum TtsVoiceMode { fullGuidance, alertsOnly, muted }

class TtsService {
  TtsVoiceMode currentMode = TtsVoiceMode.fullGuidance;
  
  // - Queue management (don't speak multiple alerts simultaneously)
  // - Platform TTS
}
