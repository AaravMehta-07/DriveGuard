import Foundation
import CarPlay

class DriveGuardCarPlaySceneDelegate: UIResponder, CPTemplateApplicationSceneDelegate {
    var interfaceController: CPInterfaceController?
    
    // Note: CarPlay navigation app entitlement required (com.apple.developer.carplay-maps)
    // BLOCKED_EXTERNAL entitlement note.
    func templateApplicationScene(_ templateApplicationScene: CPTemplateApplicationScene, didConnect interfaceController: CPInterfaceController) {
        self.interfaceController = interfaceController
        
        let mapTemplate = CPMapTemplate()
        interfaceController.setRootTemplate(mapTemplate, animated: true) { success, error in
            if success {
                let sessionManager = DriveGuardCarPlayNavigationSession(mapTemplate: mapTemplate)
                sessionManager.startSession()
            }
        }
    }
    
    func templateApplicationScene(_ templateApplicationScene: CPTemplateApplicationScene, didDisconnectInterfaceController interfaceController: CPInterfaceController) {
        self.interfaceController = nil
    }
}
