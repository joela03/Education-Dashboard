"use client"

import { useState, useEffect } from "react"
import { useRouter } from "next/navigation";
import { AppSidebar } from "@/components/app-sidebar"
import { DataTable } from "@/components/data-table"
import { SectionCards } from "@/components/section-cards";
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
  const [selectedPage, setSelectedPage] = useState("default")
  const [attendanceData, setAttendanceData] = useState<AttendanceData[]>([])
  const [PlanPaceData, setPlanPaceData] = useState<PlanPaceData[]>([])
  const [CheckupData, setCheckupData] = useState<CheckupData[]>([])
  const [progressCheckData, setProgressCheckData] = useState<ProgressCheckData[]>([])
  const [loading, setLoading] = useState(false)

  const fetchAPIData = async <T,>(endpoint: string, setData: React.Dispatch<React.SetStateAction<T[]>>) => {
    setLoading(true);
    try {
      const response = await fetch(`http://localhost:5000/${endpoint}`);
      const data = await response.json();
      setData(data);
    } catch (error) {
      console.error(`Error fetching ${endpoint} data:`, error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    const token = localStorage.getItem("token");
    if (!token) {
      router.push("/dashboard");
    } else {
      setIsAuthenticated(true)
    }
  }, [router]);

  useEffect(() => {
    if (!isAuthenticated) return;

    const lastSegment = selectedPage.split("/").pop();
    if (lastSegment === "attendance") {
      fetchAPIData(lastSegment, setAttendanceData);
    } else if (lastSegment === "progress_check") {
      fetchAPIData(lastSegment, setProgressCheckData);
    } else if (lastSegment === "planpace") {
      fetchAPIData(lastSegment, setPlanPaceData);
    } else if (lastSegment === "checkup") {
      fetchAPIData(lastSegment, setCheckupData);
    }
  }, [selectedPage]);

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
            <SectionCards />
          ) : selectedPage === "/dashboard/risk/attendance" ? (
            loading ? (
              <p>Loading Attendance data...</p>
            ) : (
              <DataTable columns={attendanceColumns} data={attendanceData} />
            )
          ) : selectedPage === "/dashboard/edu/progress_check" ? (
            loading ? (
              <p>Loading Progress Check data...</p>
            ) : (
              <DataTable columns={progressCheckColumns} data={progressCheckData} />
            )
          ) : selectedPage === "/dashboard/edu/planpace" ? (
            loading ? (
              <p>Loading Plan Pace data...</p>
            ) : (
              <DataTable columns={planPaceColumns} data={PlanPaceData} />
            )
          ) : selectedPage === "/dashboard/edu/checkup" ? (
            loading ? (
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
