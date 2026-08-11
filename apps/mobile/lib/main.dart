import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'core/theme/app_theme.dart';
import 'core/router/app_router.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  // TODO: Initialize Sentry
  // TODO: Setup Deep link handling
  runApp(
    const ProviderScope(
      child: DriveGuardApp(),
    ),
  );
}

class DriveGuardApp extends ConsumerWidget {
  const DriveGuardApp({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    return MaterialApp.router(
      title: 'DriveGuard',
      theme: lightTheme(),
      darkTheme: darkTheme(),
      themeMode: ThemeMode.system, // auto by default
      routerConfig: appRouter,
    );
  }
}
