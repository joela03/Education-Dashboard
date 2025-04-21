"use client"

import { useState, useEffect } from "react"
import { useRouter } from "next/navigation";
import { AppSidebar } from "@/components/app-sidebar"
import { DataTable } from "@/components/data-table"
import { SectionCards } from "@/components/section-cards";
import { StudentProgressChart } from "@/components/StudentProgressChart";
import {
  SidebarInset,
  SidebarProvider,
  SidebarTrigger,
} from "@/components/ui/sidebar"
import {
  Breadcrumb,
  BreadcrumbItem,
  BreadcrumbLink,
  BreadcrumbList,
} from "@/components/ui/breadcrumb"
import { attendanceColumns, AttendanceData, progressCheckColumns,
        ProgressCheckData,planPaceColumns, PlanPaceData,
        checkupColumns, CheckupData } from "@/configs/tableConfigs"

type EnrolmentStatsData = {
  active_enrolment: number;
  avg_attendance: string;
  on_hold: number;
  pre_enroled: number;
  previous_month_enrolments: number;
};

function isAttendanceData(data: any): data is AttendanceData {
  return (
    typeof data?.name === 'string' &&
    typeof data?.mathnasium_id === 'string' &&
    typeof data?.attendance_count === 'number'
  );
}

function isProgressCheckData(data: any): data is ProgressCheckData {
  return (
    typeof data?.name === 'string' &&
    typeof data?.mathnasium_id === 'string' &&
    !isNaN(Number(data?.skills_mastered_percent)) 
  );
};

function isPlanPaceData(data: any): data is PlanPaceData {
  return (
    typeof data?.name === 'string' &&
    typeof data?.mathnasium_id === 'string' &&
    typeof data?.expected_plan_percentage === 'string'
  );
}

function isCheckupData(data: any): data is CheckupData {
  return (
    typeof data?.name === 'string' &&
    typeof data?.mathnasium_id === 'string' &&
    data?.last_assessment instanceof Date
  );
}

function isEnrolmentStatsData(data: any): data is EnrolmentStatsData {
  return (
    typeof data?.active_enrolment === 'number' &&
    typeof data?.avg_attendance === 'string' &&
    typeof data?.on_hold === 'number'
  );
}

export default function Page() {
  const [isAuthenticated, setIsAuthenticated] = useState(false)
  const router = useRouter()
  const [selectedPage, setSelectedPage] = useState("/dashboard/general")
  const [attendanceData, setAttendanceData] = useState<AttendanceData[]>([])
  const [PlanPaceData, setPlanPaceData] = useState<PlanPaceData[]>([])
  const [CheckupData, setCheckupData] = useState<CheckupData[]>([])
  const [progressCheckData, setProgressCheckData] = useState<ProgressCheckData[]>([])
  const [studentData, setStudentData] = useState<any[]>([])
  const [statsData, setEnrolmentStatsData] = useState<EnrolmentStatsData[]>([])
  const [loading, setLoading] = useState({
    general: false,
    attendance: false,
    progressCheck: false,
    planpace: false,
    checkup: false,
    stats: false
  })

  const fetchArrayData = async <T,>(
    endpoint: string,
    setData: React.Dispatch<React.SetStateAction<T[]>>,
  ) => {
    setLoading(prev => ({...prev}));
    try {
      const response = await fetch(`http://localhost:5000/${endpoint}`);
      if (!response.ok) throw new Error(`Failed to fetch ${endpoint} data`);
      const data = await response.json();
      console.log(data);
      
      if (!Array.isArray(data)) {
        throw new Error(`Expected array from ${endpoint}, got ${typeof data}`);
      }

      setData(data as T[]);
    } catch (error) {
      console.error(`Error fetching ${endpoint} data:`, error);
      setData([]);
    } finally {
      setLoading(prev => ({...prev}));
    }
  };

  const fetchAttendanceData = async () => {
    return fetchArrayData<AttendanceData>(
      "attendance",
      setAttendanceData
    );
  };

  const fetchProgressCheckData = async () => {
    return fetchArrayData<ProgressCheckData>(
      "progress_check",
      setProgressCheckData
    );
  };

  const fetchPlanPaceData = async () => {
    return fetchArrayData<PlanPaceData>(
      "planpace",
      setPlanPaceData
    );
  };

  const fetchCheckupData = async () => {
    return fetchArrayData<CheckupData>(
      "checkup",
      setCheckupData
    );
  };

  const fetchStudentData = async () => {
    return fetchArrayData<any>(
      "education_stats",
      setStudentData
    );
  };

  const fetchEnrolmentStats = async () => {
    return fetchArrayData<EnrolmentStatsData>(
      "enrolment_stats",
      setEnrolmentStatsData
    );
  };

  useEffect(() => {
    const token = localStorage.getItem("token");
    if (!token) {
      router.push("/dashboard");
    } else {
      setIsAuthenticated(true);
      Promise.all([
        fetchStudentData(),
        fetchEnrolmentStats()
      ]);
    }
  }, [router]);

  useEffect(() => {
    if (!isAuthenticated) return;

    const endpointHandlers: Record<string, () => Promise<void>> = {
      "attendance": fetchAttendanceData,
      "progress_check": fetchProgressCheckData,
      "planpace": fetchPlanPaceData,
      "checkup": fetchCheckupData
    };

    const lastSegment = selectedPage.split("/").pop();
    if (lastSegment && endpointHandlers[lastSegment]) {
      endpointHandlers[lastSegment]();
    }
  }, [selectedPage, isAuthenticated]);

  if (!isAuthenticated) {
    return null;
  }

  return (
    <SidebarProvider>
      <AppSidebar onSelectPage={setSelectedPage} selectedPage={selectedPage} />
      <SidebarInset>
        <header className="flex h-16 shrink-0 items-center gap-2 bg-black text-white px-4">
          <SidebarTrigger className="-ml-1" />
          <Breadcrumb>
            <BreadcrumbList>
              <BreadcrumbItem className="hidden md:block">
                <BreadcrumbLink href="#" 
                className="px-4 py-3 text-center text-lg font-bold text-light-red-700 uppercase tracking-wider">
                  Mathnasium Dashboard
                </BreadcrumbLink>
              </BreadcrumbItem>
            </BreadcrumbList>
          </Breadcrumb>
        </header>
        <div className="flex flex-1 flex-col gap-4 p-4">
          {selectedPage === "/dashboard/general" ? (
            <div className="space-y-6">
              {loading.stats ? (
                <p>Loading stats data...</p>
              ) : statsData.length > 0 ? (
                <SectionCards stats={statsData[0]} />
              ) : (
                <p>No stats data available</p>
              )}
              <div className="bg-white p-6 rounded-lg shadow">
                <h2 className="text-2xl font-bold mb-6">Student Progress Overview</h2>
                {loading.general ? (
                  <p>Loading student progress data...</p>
                ) : (
                  <StudentProgressChart data={studentData} />
                )}
              </div>
            </div>
          ) : selectedPage === "/dashboard/risk/attendance" ? (
            loading.attendance ? (
              <p>Loading Attendance data...</p>
            ) : (
              <DataTable columns={attendanceColumns} data={attendanceData} />
            )
          ) : selectedPage === "/dashboard/edu/progress_check" ? (
            loading.progressCheck ? (
              <p>Loading Progress Check data...</p>
            ) : (
              <DataTable columns={progressCheckColumns} data={progressCheckData} />
            )
          ) : selectedPage === "/dashboard/edu/planpace" ? (
            loading.planpace ? (
              <p>Loading Plan Pace data...</p>
            ) : (
              <DataTable columns={planPaceColumns} data={PlanPaceData} />
            )
          ) : selectedPage === "/dashboard/edu/checkup" ? (
            loading.checkup ? (
              <p>Loading Checkup data...</p>
            ) : (
              <DataTable columns={checkupColumns} data={CheckupData} />
            )
          ) : (
            <div className="bg-muted/50 min-h-[100vh] flex-1 rounded-xl md:min-h-min">
              Select a section from the sidebar
            </div>
          )}
        </div>
      </SidebarInset>
    </SidebarProvider>
  );
}