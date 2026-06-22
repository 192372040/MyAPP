import 'package:flutter/material.dart';
import 'package:zego_uikit_prebuilt_call/zego_uikit_prebuilt_call.dart';
class VideoCallScreen extends StatelessWidget {
  final String userId;
  final String userName;
  final String callId;

  const VideoCallScreen({
    super.key,
    required this.userId,
    required this.userName,
    required this.callId,
  });
  
  @override
  Widget build(BuildContext context) {
    return ZegoUIKitPrebuiltCall(
      appID: 368759900,
      appSign: 'a172d12443a467cefefb7a8b877d2df3af122c8e6f5ad916d6d3fbfa740aea7b',
      userID: userId,
      userName: userName,
      callID: callId,
      config: ZegoUIKitPrebuiltCallConfig.oneOnOneVideoCall(),
    );
  }
}
