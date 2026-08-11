import 'package:flutter_riverpod/flutter_riverpod.dart';

final featureFlagsProvider = Provider((ref) => FeatureFlagsProvider());

class FeatureFlagsProvider {
  bool get dashcamAiEnabled => false;
}
