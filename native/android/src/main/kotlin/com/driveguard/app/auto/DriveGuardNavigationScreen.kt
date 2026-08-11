package com.driveguard.app.auto

import androidx.car.app.CarContext
import androidx.car.app.Screen
import androidx.car.app.model.Action
import androidx.car.app.model.CarColor
import androidx.car.app.model.CarIcon
import androidx.car.app.model.Template
import androidx.car.app.navigation.model.NavigationTemplate
import androidx.car.app.navigation.model.RoutingInfo
import androidx.car.app.navigation.model.Step
import androidx.car.app.navigation.model.TravelEstimate
import androidx.car.app.model.Distance
import androidx.car.app.model.DateTimeWithZone
import java.util.TimeZone

class DriveGuardNavigationScreen(carContext: CarContext) : Screen(carContext) {

    override fun onGetTemplate(): Template {
        val routingInfo = RoutingInfo.Builder()
            .setCurrentStep(
                Step.Builder()
                    .setCue("Turn right onto Main St. Speed limit: 50 km/h")
                    .build(),
                Distance.create(100.0, Distance.UNIT_METERS)
            )
            .build()

        return NavigationTemplate.Builder()
            .setNavigationInfo(routingInfo)
            .setDestinationTravelEstimate(
                TravelEstimate.Builder(
                    Distance.create(5.2, Distance.UNIT_KILOMETERS),
                    DateTimeWithZone.create(
                        System.currentTimeMillis() + 600000,
                        TimeZone.getDefault()
                    )
                ).build()
            )
            .setActionStrip(
                androidx.car.app.model.ActionStrip.Builder()
                    .addAction(Action.APP_ICON)
                    .build()
            )
            .build()
    }
}
