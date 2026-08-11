import Foundation
import CoreLocation

class DriveGuardLocationManager: NSObject, CLLocationManagerDelegate {
    private let locationManager = CLLocationManager()
    
    override init() {
        super.init()
        locationManager.delegate = self
        locationManager.desiredAccuracy = kCLLocationAccuracyBestForNavigation
        locationManager.distanceFilter = 10
        locationManager.allowsBackgroundLocationUpdates = true
        locationManager.pausesLocationUpdatesAutomatically = false
        locationManager.activityType = .automotiveNavigation
    }
    
    func startTracking() {
        locationManager.requestAlwaysAuthorization()
        locationManager.startUpdatingLocation()
    }
    
    func stopTracking() {
        locationManager.stopUpdatingLocation()
    }
    
    func locationManager(_ manager: CLLocationManager, didUpdateLocations locations: [CLLocation]) {
        guard let location = locations.last else { return }
        // Handle background location update
        // Send location back to main navigation engine
    }
    
    func locationManager(_ manager: CLLocationManager, didFailWithError error: Error) {
        print("DriveGuard Location tracking failed: \(error.localizedDescription)")
    }
}
