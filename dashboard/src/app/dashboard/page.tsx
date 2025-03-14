"use client"

import { useState, useEffect } from "react"
import { AppSidebar } from "@/components/app-sidebar"
import {
  Breadcrumb,
  BreadcrumbItem,
  BreadcrumbLink,
  BreadcrumbList,
  BreadcrumbPage,
  BreadcrumbSeparator,
} from "@/components/ui/breadcrumb"
import { Separator } from "@/components/ui/separator"
import {
  SidebarInset,
  SidebarProvider,
  SidebarTrigger,
} from "@/components/ui/sidebar"

export default function Page() {
  const [selectedPage, setSelectedPage] = useState("default")
  const [attendanceData, setAttendanceData] = useState(null)
  const [loading, setLoading] = useState(false)

  // Function to fetch attendance data
  const fetchAttendanceData = async () => {
    setLoading(true)
    try {
      const response = await fetch("/attendance")
      const data = await response.json()
      setAttendanceData(data)
    } catch (error) {
      console.error("Error fetching attendance data:", error)
    } finally {
      setLoading(false)
    }
  }

  // Fetch data when "Attendance" is selected
  useEffect(() => {
    if (selectedPage === "/dashboard/risk/attendance") {
      fetchAttendanceData()
    }
  }, [selectedPage])

  return (
    <SidebarProvider>
      <AppSidebar onSelectPage={setSelectedPage} />
      <SidebarInset>
        <header className="flex h-16 shrink-0 items-center gap-2 border-b px-4">
          <SidebarTrigger className="-ml-1" />
          <Separator orientation="vertical" className="mr-2 h-4" />
          <Breadcrumb>
            <BreadcrumbList>
              <BreadcrumbItem className="hidden md:block">
                <BreadcrumbLink href="#">Dashboard</BreadcrumbLink>
              </BreadcrumbItem>
              <BreadcrumbSeparator className="hidden md:block" />
              <BreadcrumbItem>
                <BreadcrumbPage>{selectedPage}</BreadcrumbPage>
              </BreadcrumbItem>
            </BreadcrumbList>
          </Breadcrumb>
        </header>
        <div className="flex flex-1 flex-col gap-4 p-4">
          {selectedPage === "/dashboard/risk/attendance" ? (
            loading ? (
              <p>Loading attendance data...</p>
            ) : attendanceData ? (
              <pre className="bg-gray-100 p-4 rounded-lg">
                {JSON.stringify(attendanceData, null, 2)}
              </pre>
            ) : (
              <p>No attendance data available.</p>
            )
          ) : (
            <div className="bg-muted/50 min-h-[100vh] flex-1 rounded-xl md:min-h-min">
              Select a section from the sidebar
            </div>
          )}
        </div>
      </SidebarInset>
    </SidebarProvider>
  )
}