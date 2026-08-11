import Foundation
import AVFoundation

class DriveGuardAudioSession {
    static let shared = DriveGuardAudioSession()
    
    func setupNavigationAudio() {
        let audioSession = AVAudioSession.sharedInstance()
        do {
            // Setup for voice guidance ducking / interrupt
            try audioSession.setCategory(
                .playback,
                mode: .voicePrompt,
                options: [.duckOthers, .interruptSpokenAudioAndMixWithOthers]
            )
            try audioSession.setActive(true, options: .notifyOthersOnDeactivation)
        } catch {
            print("Failed to set audio session category: \(error)")
        }
    }
    
    func stopNavigationAudio() {
        let audioSession = AVAudioSession.sharedInstance()
        do {
            try audioSession.setActive(false, options: .notifyOthersOnDeactivation)
        } catch {
            print("Failed to deactivate audio session: \(error)")
        }
    }
}
