import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:driveguard/features/home/home_screen.dart';
import 'package:driveguard/features/navigation/navigation_screen.dart';
import 'package:driveguard/features/navigation/copilot_screen.dart';

void main() {
  testWidgets('DriveGuard Home Screen renders map and search bar', (WidgetTester tester) async {
    await tester.pumpWidget(
      const ProviderScope(
        child: MaterialApp(
          home: HomeScreen(),
        ),
      ),
    );

    expect(find.byType(HomeScreen), findsOneWidget);
    expect(find.text('Where to?'), findsOneWidget);
  });

  testWidgets('Copilot Screen renders active status pill and stop button', (WidgetTester tester) async {
    await tester.pumpWidget(
      const ProviderScope(
        child: MaterialApp(
          home: CopilotScreen(),
        ),
      ),
    );

    expect(find.byType(CopilotScreen), findsOneWidget);
    expect(find.text('Stop Copilot'), findsOneWidget);
  });
}
