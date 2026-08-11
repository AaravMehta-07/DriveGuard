import 'package:flutter_riverpod/flutter_riverpod.dart';

final authProvider = Provider((ref) => AuthProvider());

class AuthProvider {
  bool get isAuthenticated => false;
}
