import 'package:flutter/material.dart';
import 'tokens.dart';

ThemeData lightTheme() {
  return ThemeData(
    useMaterial3: true,
    colorScheme: DriveGuardColors.light,
  );
}

ThemeData darkTheme() {
  return ThemeData(
    useMaterial3: true,
    colorScheme: DriveGuardColors.dark,
  );
}
