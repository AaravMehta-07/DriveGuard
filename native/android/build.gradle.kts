plugins {
    id("com.android.application")
    id("org.jetbrains.kotlin.android")
}

android {
    namespace = "com.driveguard.app"
    compileSdk = 34

    defaultConfig {
        applicationId = "com.driveguard.app"
        minSdk = 26
        targetSdk = 34
        versionCode = 1
        versionName = "1.0"
    }
}

dependencies {
    implementation("androidx.core:core-ktx:1.12.0")
    implementation("androidx.car.app:app:1.3.0-rc01")
    implementation("com.google.android.gms:play-services-location:21.1.0")
}
