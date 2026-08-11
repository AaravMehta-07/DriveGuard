import 'package:flutter/material.dart';

class DriveGuardColors {
  static const Color brandAccent = Color(0xFF1E88E5);
  
  static const Color warningAmber = Color(0xFFFFA000);
  static const Color criticalRed = Color(0xFFD32F2F);
  static const Color verifiedGreen = Color(0xFF388E3C);
  static const Color probableAmber = Color(0xFFF57C00);
  static const Color reportedGray = Color(0xFF757575);

  static const Color overlayScrim = Colors.black54;
  
  // Theme variants will be populated in app_theme
  static const ColorScheme light = ColorScheme.light(
    primary: brandAccent,
    secondary: warningAmber,
    error: criticalRed,
  );
  
  static const ColorScheme dark = ColorScheme.dark(
    primary: brandAccent,
    secondary: warningAmber,
    error: criticalRed,
  );
}

class DriveGuardSpacing {
  static const double s4 = 4;
  static const double s8 = 8;
  static const double s12 = 12;
  static const double s16 = 16;
  static const double s20 = 20;
  static const double s24 = 24;
  static const double s32 = 32;
  static const double s40 = 40;
  static const double s48 = 48;
  static const double s64 = 64;
}

class DriveGuardRadii {
  static const double small = 8;
  static const double medium = 12;
  static const double large = 16;
  static const double pill = 24; // 24+ for pill shape
}

class DriveGuardElevation {
  static const double e0 = 0;
  static const double e1 = 1;
  static const double e2 = 2;
  static const double e4 = 4;
  static const double e8 = 8;
}

class DriveGuardAnimation {
  static const Duration fast = Duration(milliseconds: 150);
  static const Duration normal = Duration(milliseconds: 250);
  static const Duration slow = Duration(milliseconds: 350);
}

class DriveGuardSizes {
  static const double minTouchTarget = 48;
  static const double iconSm = 16;
  static const double iconMd = 20;
  static const double iconLg = 24;
  static const double iconXl = 32;
}
