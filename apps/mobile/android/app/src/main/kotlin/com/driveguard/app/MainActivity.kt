package com.driveguard.app

import android.app.Service
import android.content.Intent
import android.os.IBinder
import androidx.annotation.NonNull
import io.flutter.embedding.android.FlutterActivity
import io.flutter.embedding.engine.FlutterEngine
import io.flutter.plugin.common.MethodChannel
import androidx.car.app.CarAppService
import androidx.car.app.Session
import androidx.car.app.validation.HostValidator

class MainActivity: FlutterActivity() {
    private val CHANNEL = "com.driveguard.app/native"

    override fun configureFlutterEngine(@NonNull flutterEngine: FlutterEngine) {
        super.configureFlutterEngine(flutterEngine)
        MethodChannel(flutterEngine.dartExecutor.binaryMessenger, CHANNEL).setMethodCallHandler { call, result ->
            when (call.method) {
                "requestAudioFocus" -> {
                    // TODO: Implement Audio Focus
                    result.success(true)
                }
                "startForegroundLocation" -> {
                    // TODO: Start DriveGuardForegroundService
                    result.success(true)
                }
                else -> {
                    result.notImplemented()
                }
            }
        }
    }
}

class DriveGuardForegroundService : Service() {
    override fun onBind(intent: Intent?): IBinder? = null
}

class DriveGuardAutoService : CarAppService() {
    override fun createHostValidator(): HostValidator {
        return HostValidator.ALLOW_ALL_HOSTS_VALIDATOR
    }

    override fun onCreateSession(): Session {
        return object : Session() {
            override fun onCreateScreen(intent: Intent): androidx.car.app.Screen {
                return object : androidx.car.app.Screen(carContext) {
                    override fun onGetTemplate(): androidx.car.app.model.Template {
                        return androidx.car.app.model.PaneTemplate.Builder(
                            androidx.car.app.model.Pane.Builder().build()
                        ).setTitle("DriveGuard").build()
                    }
                }
            }
        }
    }
}
