import 'package:flutter/widgets.dart';

/// Central viewport insets model for map positioning and bounds calculations.
/// Ensures map camera fit/recenter/overview operations honor screen overlays
/// (top maneuver card, bottom ETA panel, active bottom sheet, system status bar).
///
/// Per Correction #30: No route, camera, or destination marker will be obscured
/// beneath floating cards or expanded sheets after a fit/recenter operation.
class MapViewportInsets {

  const MapViewportInsets({
    this.topManeuverCardHeight = 0.0,
    this.bottomEtaFooterHeight = 0.0,
    this.activeBottomSheetHeight = 0.0,
    this.speedPanelWidth = 0.0,
    this.systemTopSafeArea = 0.0,
    this.systemBottomSafeArea = 0.0,
  });

  /// Creates insets derived from current MediaQuery padding and UI element dimensions.
  factory MapViewportInsets.fromContext(
    BuildContext context, {
    double topManeuverCardHeight = 0.0,
    double bottomEtaFooterHeight = 0.0,
    double activeBottomSheetHeight = 0.0,
    double speedPanelWidth = 0.0,
  }) {
    final padding = MediaQuery.of(context).padding;
    return MapViewportInsets(
      topManeuverCardHeight: topManeuverCardHeight,
      bottomEtaFooterHeight: bottomEtaFooterHeight,
      activeBottomSheetHeight: activeBottomSheetHeight,
      speedPanelWidth: speedPanelWidth,
      systemTopSafeArea: padding.top,
      systemBottomSafeArea: padding.bottom,
    );
  }
  final double topManeuverCardHeight;
  final double bottomEtaFooterHeight;
  final double activeBottomSheetHeight;
  final double speedPanelWidth;
  final double systemTopSafeArea;
  final double systemBottomSafeArea;

  /// Total top padding required for map camera positioning.
  double get totalTopInset => systemTopSafeArea + topManeuverCardHeight + 16.0;

  /// Total bottom padding required for map camera positioning.
  double get totalBottomInset =>
      systemBottomSafeArea +
      (activeBottomSheetHeight > 0.0
          ? activeBottomSheetHeight
          : bottomEtaFooterHeight) +
      16.0;

  /// Total left padding required for map camera positioning.
  double get totalLeftInset => 16.0;

  /// Total right padding required for map camera positioning.
  double get totalRightInset => 16.0;

  /// Convert to EdgeInsets padding for map controller camera padding calls.
  EdgeInsets toEdgeInsets() {
    return EdgeInsets.fromLTRB(
      totalLeftInset,
      totalTopInset,
      totalRightInset,
      totalBottomInset,
    );
  }

  MapViewportInsets copyWith({
    double? topManeuverCardHeight,
    double? bottomEtaFooterHeight,
    double? activeBottomSheetHeight,
    double? speedPanelWidth,
    double? systemTopSafeArea,
    double? systemBottomSafeArea,
  }) {
    return MapViewportInsets(
      topManeuverCardHeight:
          topManeuverCardHeight ?? this.topManeuverCardHeight,
      bottomEtaFooterHeight:
          bottomEtaFooterHeight ?? this.bottomEtaFooterHeight,
      activeBottomSheetHeight:
          activeBottomSheetHeight ?? this.activeBottomSheetHeight,
      speedPanelWidth: speedPanelWidth ?? this.speedPanelWidth,
      systemTopSafeArea: systemTopSafeArea ?? this.systemTopSafeArea,
      systemBottomSafeArea:
          systemBottomSafeArea ?? this.systemBottomSafeArea,
    );
  }
}
