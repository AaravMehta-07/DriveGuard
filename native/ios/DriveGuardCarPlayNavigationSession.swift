import Foundation
import CarPlay
import MapKit

class DriveGuardCarPlayNavigationSession {
    private let mapTemplate: CPMapTemplate
    private var navigationSession: CPNavigationSession?
    
    init(mapTemplate: CPMapTemplate) {
        self.mapTemplate = mapTemplate
    }
    
    func startSession() {
        let trip = CPTrip(origin: MKMapItem(), destination: MKMapItem(), routeChoices: [])
        
        mapTemplate.showTripPreviews([trip], textConfiguration: nil)
        
        // Start actual navigation when selected
        navigationSession = mapTemplate.startNavigationSession(for: trip)
        
        updateManeuver()
    }
    
    private func updateManeuver() {
        let maneuver = CPManeuver()
        // DriveGuard alerts
        maneuver.instructionVariants = ["Speed Camera ahead, limit 50 km/h"]
        
        let travelEstimates = CPTravelEstimates(distanceRemaining: Measurement(value: 5.2, unit: .kilometers), timeRemaining: 600)
        
        navigationSession?.updateEstimates(travelEstimates, for: maneuver)
    }
    
    func stopSession() {
        navigationSession?.finish()
        navigationSession = nil
    }
}
