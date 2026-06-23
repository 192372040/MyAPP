import 'package:flutter/material.dart';
import 'package:zego_uikit_prebuilt_call/zego_uikit_prebuilt_call.dart';

class DoctorVideoCallScreen extends StatelessWidget {
  final String callID;
  final String doctorId;
  final String doctorName;

  const DoctorVideoCallScreen({
    super.key,
    required this.callID,
    required this.doctorId,
    required this.doctorName,
  });

  @override
  Widget build(BuildContext context) {
    return ZegoUIKitPrebuiltCall(
      appID:  368759900,
      appSign: 'a172d12443a467cefefb7a8b877d2df3af122c8e6f5ad916d6d3fbfa740aea7b',

      userID: doctorId,
      userName: doctorName,

      callID: callID,

      config: ZegoUIKitPrebuiltCallConfig.oneOnOneVideoCall(),
    );
  }
}