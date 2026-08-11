import 'package:flutter/material.dart';

class OfflineScreen extends StatelessWidget {
  const OfflineScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('OfflineScreen')),
      body: const Center(child: Text('OfflineScreen Content')),
    );
  }
}
