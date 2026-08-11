import 'package:flutter/material.dart';

class DiagnosticScreen extends StatelessWidget {
  const DiagnosticScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('DiagnosticScreen')),
      body: const Center(child: Text('DiagnosticScreen Content')),
    );
  }
}
