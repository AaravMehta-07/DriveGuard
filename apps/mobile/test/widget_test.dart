import 'package:flutter_test/flutter_test.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

void main() {
  group('DriveGuard Mobile Unit & Provider Tests', () {
    test('ProviderScope container initializes cleanly', () {
      final container = ProviderContainer();
      addTearDown(container.dispose);
      expect(container, isNotNull);
    });

    test('DriveGuard app configuration sanity check', () {
      const appName = 'DriveGuard';
      const version = '1.0.0';
      expect(appName, equals('DriveGuard'));
      expect(version, isNotEmpty);
    });
  });
}
