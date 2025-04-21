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

export default function Page() {
  const [isAuthenticated, setIsAuthenticated] = useState(false)
  const router = useRouter()
  const [selectedPage, setSelectedPage] = useState("/dashboard/general")
  const [attendanceData, setAttendanceData] = useState<AttendanceData[]>([])
  const [PlanPaceData, setPlanPaceData] = useState<PlanPaceData[]>([])
  const [CheckupData, setCheckupData] = useState<CheckupData[]>([])
  const [progressCheckData, setProgressCheckData] = useState<ProgressCheckData[]>([])
  const [studentData, setStudentData] = useState<any[]>([])
  const [loading, setLoading] = useState({
    general: false,
    attendance: false,
    progressCheck: false,
    planpace: false,
  })

  const fetchAPIData = async <T,>(
    endpoint: string,
    setData: React.Dispatch<React.SetStateAction<T | T[]>>,
    loadingKey: keyof typeof loading
  ) => {
    setLoading(prev => ({...prev, [loadingKey]: true}));
    try {
      const response = await fetch(`http://localhost:5000/${endpoint}`);
      if (!response.ok) throw new Error(`Failed to fetch ${endpoint} data`)
      const data = await response.json();
      setData(data);
    } catch (error) {
      console.error(`Error fetching ${endpoint} data:`, error);
    } finally {
      setLoading(prev => ({...prev, [loadingKey]: false}));
    }
  };

  const fetchStudentProgressData = async () => {
    setLoading(prev => ({...prev, general: true}));
    try {
      const response = await fetch('http://localhost:5000/education_stats');
      if (!response.ok) throw new Error('Failed to fetch student data');
      const data = await response.json();
      setStudentData(data);
    } catch (error) {
      console.error('Error fetching student data:', error);
    } finally {
      setLoading(prev => ({...prev, general: false}));
    }
  };

  useEffect(() => {
    const token = localStorage.getItem("token");
    if (!token) {
      router.push("/dashboard");
    } else {
      setIsAuthenticated(true)
      fetchStudentProgressData();
    }
  }, [router]);

  useEffect(() => {
    if (!isAuthenticated) return;

    const lastSegment = selectedPage.split("/").pop();
    if (lastSegment === "attendance") {
      fetchAPIData(lastSegment, setAttendanceData, 'attendance');
    } else if (lastSegment === "progress_check") {
      fetchAPIData(lastSegment, setProgressCheckData, 'progressCheck');
    } else if (lastSegment === "planpace") {
      fetchAPIData(lastSegment, setPlanPaceData, 'planpace');
    } else if (lastSegment === "checkup") {
      fetchAPIData(lastSegment, setCheckupData, 'checkup');
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
              <SectionCards />
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