import 'package:flutter/material.dart';
import '../Patientdashboard/services/api_service.dart';
import 'package:my_project/Admin/AdProfile.dart';
import 'package:my_project/Admin/BedsS.dart';
import 'package:my_project/Admin/Doctors.dart';
import 'package:my_project/Admin/Analytis.dart';
import 'package:my_project/Admin/HospitalAppointmentsScreen.dart';
class HospitalDashboardScreen extends StatefulWidget {
  final String hospitalId;

const HospitalDashboardScreen({

  Key? key,
  required this.hospitalId,

}) : super(key: key);
@override
State<HospitalDashboardScreen>
createState() =>
_HospitalDashboardScreenState();
}

class _HospitalDashboardScreenState
extends State<HospitalDashboardScreen> {
int currentIndex = 0;
Map<String, dynamic>? hospitalData;

bool isLoading = true;

@override
void initState() {

  super.initState();

  fetchHospitalData();
}

  Future<void> fetchHospitalData() async {
    var res = await ApiService.getAdminHospitalSummary(widget.hospitalId);
    var analyticsRes = await ApiService.getHospitalAnalytics(widget.hospitalId);

  setState(() {
    hospitalData = res["hospital"];
    if (analyticsRes["success"] == true) {
      hospitalData ??= {};
      hospitalData!['total_doctors'] = analyticsRes['total_doctors'];
      hospitalData!['total_beds'] = analyticsRes['total_beds'];
      hospitalData!['total_departments'] = analyticsRes['total_departments'];
      hospitalData!['today_appointments'] = analyticsRes['today_appointments'];
    }
    isLoading = false;
  });
}

@override
Widget build(BuildContext context) {
    const Color bgColor = Color(0xFF252525);
    const Color primaryColor = Color(0xFFC7781E);
    const Color cardBgColor = Color(0xFF1E1E1E);
if (isLoading) {

  return const Scaffold(

    body: Center(
      child:
          CircularProgressIndicator(),
    ),
  );
}
    return Scaffold(
      backgroundColor: bgColor,
      appBar: AppBar(
        backgroundColor: bgColor,
        elevation: 0,
        toolbarHeight: 80,
        leadingWidth: 70,
        leading: Padding(
          padding: const EdgeInsets.only(left: 16.0, top: 12, bottom: 12),
          child: CircleAvatar(
            backgroundColor: primaryColor,
            child: Text(

  hospitalData?['hospital_name']
          ?.substring(0, 2)
          .toUpperCase()
      ?? '',

  style: const TextStyle(

    color: Colors.white,
    fontWeight: FontWeight.bold,

  ),
),
          ),
        ),
        title: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
           Text(

  hospitalData?['hospital_name']
      ?? '',

  style: const TextStyle(
    color: Colors.white,
    fontSize: 16,
    fontWeight: FontWeight.bold,
  ),
),
           Text(

  widget.hospitalId,

  style: TextStyle(
    color: primaryColor,
    fontSize: 12,
  ),
),
          ],
        ),
        actions: [
          Padding(
            padding: const EdgeInsets.only(right: 16.0),
            child: Center(
              child: GestureDetector(
                onTap: () {
                  showModalBottomSheet(
                    context: context,
                    backgroundColor: const Color(0xFF1E1E1E),
                    shape: const RoundedRectangleBorder(
                      borderRadius: BorderRadius.vertical(top: Radius.circular(20)),
                    ),
                    builder: (context) {
                      return Container(
                        padding: const EdgeInsets.all(20),
                        child: Column(
                          mainAxisSize: MainAxisSize.min,
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            const Text('Notifications', style: TextStyle(color: Colors.white, fontSize: 20, fontWeight: FontWeight.bold)),
                            const SizedBox(height: 20),
                            const Center(child: Text('No new notifications', style: TextStyle(color: Colors.grey))),
                            const SizedBox(height: 40),
                          ],
                        ),
                      );
                    },
                  );
                },
                child: Stack(
                  children: [
                    Container(
                      width: 40,
                      height: 40,
                      decoration: BoxDecoration(
                        shape: BoxShape.circle,
                        border: Border.all(color: primaryColor.withValues(alpha: 0.5), width: 1),
                      ),
                      child: const Icon(Icons.notifications_outlined, color: Colors.white, size: 20),
                    ),
                    Positioned(
                      right: 8,
                      top: 8,
                      child: Container(
                        width: 8,
                        height: 8,
                        decoration: const BoxDecoration(color: Colors.redAccent, shape: BoxShape.circle),
                      ),
                    ),
                  ],
                ),
              ),
            ),
          )
        ],
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // Divider below AppBar
            Divider(color: Colors.grey[800], height: 1),
            const SizedBox(height: 16),
            
            // Hospital Overview Card
            Container(
              padding: const EdgeInsets.all(20),
              decoration: BoxDecoration(
                color: const Color(0xFFB56A15),
                borderRadius: BorderRadius.circular(20),
              ),
              child: Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      const Text('Hospital overview', style: TextStyle(color: Colors.white70, fontSize: 14)),
                      const SizedBox(height: 4),
                      Text('${hospitalData?['total_doctors'] ?? 0} doctors', style: const TextStyle(color: Colors.white, fontSize: 28, fontWeight: FontWeight.bold)),
                      const SizedBox(height: 12),
                      Container(
                        padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
                        decoration: BoxDecoration(
                          color: Colors.white.withOpacity(0.2),
                          borderRadius: BorderRadius.circular(20),
                        ),
                        child: Text('${hospitalData?['total_beds'] ?? 0} beds • ${hospitalData?['total_departments'] ?? 0} depts', style: const TextStyle(color: Colors.white, fontSize: 12, fontWeight: FontWeight.w500)),
                      ),
                      const SizedBox(height: 20),
                      Container(
                        width: 160,
                        height: 6,
                        decoration: BoxDecoration(
                          color: Colors.black26,
                          borderRadius: BorderRadius.circular(3),
                        ),
                        alignment: Alignment.centerLeft,
                        child: Container(
                          width: 110,
                          height: 6,
                          decoration: BoxDecoration(
                            color: Colors.white,
                            borderRadius: BorderRadius.circular(3),
                          ),
                        ),
                      )
                    ],
                  ),
                  Container(
                    width: 65,
                    height: 65,
                    decoration: BoxDecoration(
                      color: Colors.white.withOpacity(0.25),
                      shape: BoxShape.circle,
                    ),
                    child: const Icon(Icons.add, color: Colors.white, size: 32),
                  )
                ],
              ),
            ),
            const SizedBox(height: 20),
            
            // Stats Grid
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                _buildStatCard('${hospitalData?['total_doctors'] ?? 0}', 'Doctors', Colors.blue[400]!, cardBgColor),
                _buildStatCard('${hospitalData?['total_beds'] ?? 0}', 'Beds', Colors.green[400]!, cardBgColor),
                _buildStatCard('${hospitalData?['total_departments'] ?? 0}', 'Depts', Colors.redAccent, cardBgColor),
                _buildStatCard('${hospitalData?['today_appointments'] ?? 0}', 'Today', primaryColor, cardBgColor),
              ],
            ),
            const SizedBox(height: 24),
            const Text('Quick actions', style: TextStyle(color: Colors.white, fontSize: 16, fontWeight: FontWeight.bold)),
            const SizedBox(height: 16),
            
            // Quick Actions Grid
            Row(
              children: [
                Expanded(
                  child: GestureDetector(
                    onTap: () => Navigator.push(context, MaterialPageRoute(builder: (_) => ManageDoctorsScreen(hospitalId: widget.hospitalId))),
                    child: _buildActionCard(Icons.person_add_outlined, 'Add doctor', Colors.blue[400]!, cardBgColor),
                  ),
                ),
                const SizedBox(width: 12),
                Expanded(
                  child: GestureDetector(
                    onTap: () => Navigator.push(context, MaterialPageRoute(builder: (_) => BedManagementScreen(hospitalId: widget.hospitalId))),
                    child: _buildActionCard(Icons.bed_outlined, 'Manage beds', Colors.green[400]!, cardBgColor),
                  ),
                ),
              ],
            ),
            const SizedBox(height: 12),
            Row(
              children: [
                Expanded(
                  child: GestureDetector(
                    onTap: () => Navigator.push(context, MaterialPageRoute(builder: (_) => HospitalAppointmentsScreen(hospitalId: widget.hospitalId))),
                    child: _buildActionCard(Icons.calendar_today_outlined, 'Appointments', primaryColor, cardBgColor),
                  ),
                ),
                const SizedBox(width: 12),
                Expanded(
                  child: GestureDetector(
                    onTap: () => Navigator.push(context, MaterialPageRoute(builder: (_) => AnalyticsScreen(hospitalId: widget.hospitalId))),
                    child: _buildActionCard(Icons.show_chart, 'Analytics', Colors.deepPurpleAccent[100]!, cardBgColor),
                  ),
                ),
              ],
            ),
            const SizedBox(height: 24),
          ],
        ),
      ),
      bottomNavigationBar: BottomNavigationBar(

  currentIndex: currentIndex,

  onTap: (index) {

    setState(() {

      currentIndex = index;
    });

    // HOME
    if (index == 0) {

      Navigator.push(

        context,

        MaterialPageRoute(

          builder: (context) =>
              HospitalDashboardScreen(

            hospitalId:
                widget.hospitalId,

          ),
        ),
      );
    }

    // DOCTORS
    else if (index == 1) {

      Navigator.push(

        context,

        MaterialPageRoute(

          builder: (context) =>
              ManageDoctorsScreen(
  hospitalId: widget.hospitalId,
),

        ),
      );
    }

    // BEDS
    else if (index == 2) {

      Navigator.push(

        context,

        MaterialPageRoute(

          builder: (context) =>
              BedManagementScreen( hospitalId: widget.hospitalId,),

        ),
      );
    }

    // ANALYTICS
    else if (index == 3) {

      Navigator.push(

        context,

        MaterialPageRoute(

          builder: (context) =>
              AnalyticsScreen( hospitalId: widget.hospitalId,),

        ),
      );
    }

    // PROFILE
    else if (index == 4) {

      Navigator.push(

        context,

        MaterialPageRoute(

          builder: (context) =>
         HospitalProfileScreen(
  hospitalData: hospitalData,
  hospitalId: widget.hospitalId,
)
        ),
      );
    }
  },

  backgroundColor:
      const Color(0xFF1E1E1E),

  type:
      BottomNavigationBarType.fixed,

  selectedItemColor:
      primaryColor,

  unselectedItemColor:
      Colors.grey,

  items: const [

    BottomNavigationBarItem(
      icon: Icon(Icons.home_outlined),
      label: 'Home',
    ),

    BottomNavigationBarItem(
      icon: Icon(Icons.person_outline),
      label: 'Doctors',
    ),

    BottomNavigationBarItem(
      icon: Icon(Icons.medical_services_outlined),
      label: 'Beds',
    ),

    BottomNavigationBarItem(
      icon: Icon(Icons.show_chart),
      label: 'Analytics',
    ),

    BottomNavigationBarItem(
      icon: Icon(Icons.circle_outlined),
      label: 'Profile',
    ),
  ],
),
    );
  }

  Widget _buildStatCard(String value, String label, Color color, Color bgColor) {
    return Expanded(
      child: Container(
        margin: const EdgeInsets.symmetric(horizontal: 4),
        padding: const EdgeInsets.symmetric(vertical: 16),
        decoration: BoxDecoration(
          color: bgColor,
          border: Border.all(color: color.withOpacity(0.5)),
          borderRadius: BorderRadius.circular(12),
        ),
        child: Column(
          children: [
            Text(value, style: const TextStyle(color: Colors.white, fontSize: 20, fontWeight: FontWeight.bold)),
            const SizedBox(height: 4),
            Text(label, style: TextStyle(color: color, fontSize: 11, fontWeight: FontWeight.w500)),
          ],
        ),
      ),
    );
  }

  Widget _buildActionCard(IconData icon, String label, Color color, Color bgColor) {
    return Container(
      padding: const EdgeInsets.symmetric(vertical: 18, horizontal: 12),
      decoration: BoxDecoration(
        color: bgColor,
        border: Border.all(color: color.withOpacity(0.5)),
        borderRadius: BorderRadius.circular(12),
      ),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          Icon(icon, color: color, size: 22),
          const SizedBox(width: 8),
          Flexible(
            child: Text(
              label,
              style: TextStyle(color: color, fontSize: 14, fontWeight: FontWeight.w600),
              overflow: TextOverflow.ellipsis,
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildAlertCard(String text, String time, Color color, Color bgColor) {
    return Container(
      padding: const EdgeInsets.all(18),
      decoration: BoxDecoration(
        color: bgColor,
        border: Border.all(color: color.withOpacity(0.5)),
        borderRadius: BorderRadius.circular(12),
      ),
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Container(
            margin: const EdgeInsets.only(top: 6, right: 12),
            width: 8,
            height: 8,
            decoration: BoxDecoration(color: color, shape: BoxShape.circle),
          ),
          Expanded(
            child: Text(
              text,
              style: const TextStyle(color: Colors.white, fontSize: 14, fontWeight: FontWeight.w600, height: 1.4),
            ),
          ),
          const SizedBox(width: 12),
          Text(
            time,
            style: TextStyle(color: color, fontSize: 12, fontWeight: FontWeight.w500),
          ),
        ],
      ),
    );
  }
}