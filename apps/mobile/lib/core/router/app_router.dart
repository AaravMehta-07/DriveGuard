import 'package:go_router/go_router.dart';
import '../../features/home/home_screen.dart';
import '../../features/search/search_screen.dart';
import '../../features/route/route_selection_screen.dart';
import '../../features/route/route_preview_screen.dart';
import '../../features/navigation/navigation_screen.dart';
import '../../features/navigation/copilot_screen.dart';
import '../../features/enforcement/enforcement_explorer_screen.dart';
import '../../features/trips/trip_history_screen.dart';
import '../../features/places/saved_places_screen.dart';
import '../../features/offline/offline_screen.dart';
import '../../features/settings/settings_screen.dart';
import '../../features/settings/vehicle_screen.dart';
import '../../features/settings/privacy_screen.dart';
import '../../features/settings/legal_screen.dart';
import '../../features/settings/notification_preferences_screen.dart';
import '../../features/account/account_screen.dart';
import '../../features/diagnostic/diagnostic_screen.dart';

final appRouter = GoRouter(
  initialLocation: '/',
  routes: [
    GoRoute(
      path: '/',
      builder: (context, state) => const HomeScreen(),
    ),
    GoRoute(
      path: '/search',
      builder: (context, state) => const SearchScreen(),
    ),
    GoRoute(
      path: '/route-selection',
      builder: (context, state) => const RouteSelectionScreen(),
    ),
    GoRoute(
      path: '/route-preview',
      builder: (context, state) => const RoutePreviewScreen(),
    ),
    GoRoute(
      path: '/navigation',
      builder: (context, state) => const NavigationScreen(),
    ),
    GoRoute(
      path: '/copilot',
      builder: (context, state) => const CopilotScreen(),
    ),
    GoRoute(
      path: '/enforcement-explorer',
      builder: (context, state) => const EnforcementExplorerScreen(),
    ),
    GoRoute(
      path: '/trip-history',
      builder: (context, state) => const TripHistoryScreen(),
    ),
    GoRoute(
      path: '/saved-places',
      builder: (context, state) => const SavedPlacesScreen(),
    ),
    GoRoute(
      path: '/offline',
      builder: (context, state) => const OfflineScreen(),
    ),
    GoRoute(
      path: '/settings',
      builder: (context, state) => const SettingsScreen(),
      routes: [
        GoRoute(
          path: 'vehicle',
          builder: (context, state) => const VehicleScreen(),
        ),
        GoRoute(
          path: 'privacy',
          builder: (context, state) => const PrivacyScreen(),
        ),
        GoRoute(
          path: 'legal',
          builder: (context, state) => const LegalScreen(),
        ),
        GoRoute(
          path: 'notifications',
          builder: (context, state) => const NotificationPreferencesScreen(),
        ),
      ]
    ),
    GoRoute(
      path: '/account',
      builder: (context, state) => const AccountScreen(),
    ),
    GoRoute(
      path: '/diagnostic',
      builder: (context, state) => const DiagnosticScreen(),
    ),
  ],
);
