import 'dart:math';

/// GPS location sample with accuracy and timestamp.
class LocationSample {

  const LocationSample({
    required this.latitude,
    required this.longitude,
    required this.speedKph,
    required this.heading,
    required this.accuracyMeters,
    required this.timestamp,
    this.altitudeMeters,
  });
  final double latitude;
  final double longitude;
  final double speedKph;
  final double heading; // 0..360 degrees
  final double accuracyMeters;
  final DateTime timestamp;
  final double? altitudeMeters;
}

/// Adaptive location filter for mobile GPS smoothing.
/// Combines exponential moving average (EMA) and speed/heading thresholding
/// to eliminate GPS jitter without introducing unacceptable latency.
class DriveGuardLocationFilter {

  DriveGuardLocationFilter({
    this.alphaSpeed = 0.3,
    this.alphaHeading = 0.25,
    this.maxValidSpeedKph = 250.0,
  });
  final double alphaSpeed;
  final double alphaHeading;
  final double maxValidSpeedKph;

  LocationSample? _previousSample;
  double _filteredSpeed = 0.0;
  double _filteredHeading = 0.0;

  LocationSample filter(LocationSample raw) {
    // Reject wildly inaccurate samples (>50m accuracy circle)
    if (raw.accuracyMeters > 50.0 && _previousSample != null) {
      return _previousSample!;
    }

    // Reject impossible speed jumps
    if (raw.speedKph > maxValidSpeedKph) {
      return _previousSample ?? raw;
    }

    if (_previousSample == null) {
      _previousSample = raw;
      _filteredSpeed = raw.speedKph;
      _filteredHeading = raw.heading;
      return raw;
    }

    // Smooth speed using EMA
    _filteredSpeed = (alphaSpeed * raw.speedKph) + ((1.0 - alphaSpeed) * _filteredSpeed);

    // Smooth heading taking angular wraparound into account
    _filteredHeading = _smoothAngle(_filteredHeading, raw.heading, alphaHeading);

    final filtered = LocationSample(
      latitude: raw.latitude,
      longitude: raw.longitude,
      speedKph: _filteredSpeed,
      heading: _filteredHeading,
      accuracyMeters: raw.accuracyMeters,
      timestamp: raw.timestamp,
      altitudeMeters: raw.altitudeMeters,
    );

    _previousSample = filtered;
    return filtered;
  }

  double _smoothAngle(double current, double target, double alpha) {
    double diff = (target - current) % 360.0;
    if (diff > 180.0) diff -= 360.0;
    if (diff < -180.0) diff += 360.0;
    return (current + (alpha * diff)) % 360.0;
  }

  void reset() {
    _previousSample = null;
    _filteredSpeed = 0.0;
    _filteredHeading = 0.0;
  }
}
