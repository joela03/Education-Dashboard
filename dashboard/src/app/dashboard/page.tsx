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
import { Button } from "@/components/ui/button"
import { RefreshCw } from "lucide-react"
import { attendanceColumns, AttendanceData, progressCheckColumns,
        ProgressCheckData, planPaceColumns, PlanPaceData,
        checkupColumns, CheckupData } from "@/configs/tableConfigs"

type EnrolmentStatsData = {
  active_enrolment: number;
  avg_attendance: string;
  on_hold: number;
  pre_enroled: number;
  previous_month_enrolments: number;
};

type ExtendedStatsData = EnrolmentStatsData & {
  needCheckup: number;
  needProgressCheck: number;
  poorAttendance: number;
};

interface CachedData<T> {
  data: T[];
  timestamp: number;
}

export default function Page() {
  const [isAuthenticated, setIsAuthenticated] = useState(false)
  const router = useRouter()
  const [selectedPage, setSelectedPage] = useState("/dashboard/general")
  const [attendanceData, setAttendanceData] = useState<AttendanceData[]>([])
  const [planPaceData, setPlanPaceData] = useState<PlanPaceData[]>([])
  const [checkupData, setCheckupData] = useState<CheckupData[]>([])
  const [progressCheckData, setProgressCheckData] = useState<ProgressCheckData[]>([])
  const [studentData, setStudentData] = useState<any[]>([])
  const [statsData, setStatsData] = useState<EnrolmentStatsData[]>([])
  const [refreshing, setRefreshing] = useState(false)
  const [loading, setLoading] = useState({
    general: false,
    attendance: false,
    progressCheck: false,
    planpace: false,
    checkup: false,
    stats: false
  })

  const CACHE_CONFIG = {
    DURATION: 24 * 60 * 60 * 1000,
    ENDPOINTS: {
      "education_stats": { duration: 12 * 60 * 60 * 1000 }, 
      "enrolment_stats": { duration: 6 * 60 * 60 * 1000 }, 
      "attendance": { duration: 24 * 60 * 60 * 1000 },
      "progress_check": { duration: 24 * 60 * 60 * 1000 },
      "planpace": { duration: 24 * 60 * 60 * 1000 },
      "checkup": { duration: 24 * 60 * 60 * 1000 }
    }
  };

  const fetchWithCache = async <T,>(
    endpoint: string,
    setData: React.Dispatch<React.SetStateAction<T[]>>,
    loadingKey: keyof typeof loading,
    forceRefresh = false
  ) => {
    const cacheKey = `mathnasium_cache_${endpoint}`;
    const now = Date.now();
    
    const cacheDuration = CACHE_CONFIG.ENDPOINTS[endpoint as keyof typeof CACHE_CONFIG.ENDPOINTS]?.duration || CACHE_CONFIG.DURATION;
    
    if (!forceRefresh) {
      try {
        const cachedItem = localStorage.getItem(cacheKey);
        if (cachedItem) {
          const { data, timestamp } = JSON.parse(cachedItem) as CachedData<T>;
          if (now - timestamp < cacheDuration) {
            console.log(`Using cached data for ${endpoint} (age: ${Math.round((now - timestamp) / 60000)} minutes)`);
            setData(data);
            return;
          } else {
            console.log(`Cache expired for ${endpoint}`);
          }
        }
      } catch (error) {
        console.error(`Error reading cache for ${endpoint}:`, error);
      }
    }

    setLoading(prev => ({...prev, [loadingKey]: true}));
    
    try {
      const response = await fetch(`http://localhost:5000/${endpoint}`);
      
      if (!response.ok) {
        throw new Error(`API returned ${response.status} for ${endpoint}`);
      }
      
      const data = await response.json();
      
      if (!Array.isArray(data)) {
        throw new Error(`Expected array from ${endpoint}, got ${typeof data}`);
      }
      
      try {
        localStorage.setItem(cacheKey, JSON.stringify({
          data,
          timestamp: now
        }));
      } catch (cacheError) {
        console.warn(`Failed to cache ${endpoint} data:`, cacheError);
      }
      
      setData(data as T[]);
      console.log(`Fetched fresh data for ${endpoint}`);
      
    } catch (error) {
      console.error(`Error fetching ${endpoint}:`, error);
      
      try {
        const cachedItem = localStorage.getItem(cacheKey);
        if (cachedItem) {
          const { data } = JSON.parse(cachedItem) as CachedData<T>;
          setData(data);
          console.log(`Using stale cache for ${endpoint} as fallback`);
        }
      } catch (fallbackError) {
        console.error(`Failed to use fallback cache for ${endpoint}:`, fallbackError);
        setData([] as unknown as T[]);
      }
    } finally {
      setLoading(prev => ({...prev, [loadingKey]: false}));
    }
  };

  const getExtendedStats = (): ExtendedStatsData | undefined => {
    if (!statsData.length) return undefined;
    
    return {
      ...statsData[0],
      needCheckup: checkupData.length,
      needProgressCheck: progressCheckData.length,
      poorAttendance: attendanceData.length
    };
  };

  const preloadAllInterventionData = async () => {
    try {
      await Promise.all([
        fetchAttendanceDataQuietly(),
        fetchProgressCheckDataQuietly(),
        fetchCheckupDataQuietly()
      ]);
    } catch (error) {
      console.error("Error preloading intervention data:", error);
    }
  };

  const fetchAttendanceData = async (forceRefresh = false) => {
    return fetchWithCache<AttendanceData>(
      "attendance",
      setAttendanceData,
      'attendance',
      forceRefresh
    );
  };

  const fetchAttendanceDataQuietly = async () => {
    const cacheKey = `mathnasium_cache_attendance`;
    try {
      const cachedItem = localStorage.getItem(cacheKey);
      if (cachedItem) {
        const { data } = JSON.parse(cachedItem) as CachedData<AttendanceData>;
        setAttendanceData(data);
        return data;
      }
      
      const response = await fetch(`http://localhost:5000/attendance`);
      if (!response.ok) return [];
      
      const data = await response.json();
      if (!Array.isArray(data)) return [];
      
      setAttendanceData(data);
      return data;
    } catch (error) {
      console.error("Error fetching attendance data quietly:", error);
      return [];
    }
  };

  const fetchProgressCheckData = async (forceRefresh = false) => {
    return fetchWithCache<ProgressCheckData>(
      "progress_check",
      setProgressCheckData,
      'progressCheck',
      forceRefresh
    );
  };

  const fetchProgressCheckDataQuietly = async () => {
    const cacheKey = `mathnasium_cache_progress_check`;
    try {
      const cachedItem = localStorage.getItem(cacheKey);
      if (cachedItem) {
        const { data } = JSON.parse(cachedItem) as CachedData<ProgressCheckData>;
        setProgressCheckData(data);
        return data;
      }
      
      const response = await fetch(`http://localhost:5000/progress_check`);
      if (!response.ok) return [];
      
      const data = await response.json();
      if (!Array.isArray(data)) return [];
      
      setProgressCheckData(data);
      return data;
    } catch (error) {
      console.error("Error fetching progress check data quietly:", error);
      return [];
    }
  };

  const fetchPlanPaceData = async (forceRefresh = false) => {
    return fetchWithCache<PlanPaceData>(
      "planpace",
      setPlanPaceData,
      'planpace',
      forceRefresh
    );
  };

  const fetchCheckupData = async (forceRefresh = false) => {
    return fetchWithCache<CheckupData>(
      "checkup",
      setCheckupData,
      'checkup',
      forceRefresh
    );
  };

  const fetchCheckupDataQuietly = async () => {
    const cacheKey = `mathnasium_cache_checkup`;
    try {
      const cachedItem = localStorage.getItem(cacheKey);
      if (cachedItem) {
        const { data } = JSON.parse(cachedItem) as CachedData<CheckupData>;
        setCheckupData(data);
        return data;
      }
      
      const response = await fetch(`http://localhost:5000/checkup`);
      if (!response.ok) return [];
      
      const data = await response.json();
      if (!Array.isArray(data)) return [];
      
      setCheckupData(data);
      return data;
    } catch (error) {
      console.error("Error fetching checkup data quietly:", error);
      return [];
    }
  };

  const fetchStudentData = async (forceRefresh = false) => {
    return fetchWithCache<any>(
      "education_stats",
      setStudentData,
      'general',
      forceRefresh
    );
  };

  const fetchEnrolmentStats = async (forceRefresh = false) => {
    return fetchWithCache<EnrolmentStatsData>(
      "enrolment_stats",
      setStatsData,
      'stats',
      forceRefresh
    );
  };

  const refreshCurrentData = async () => {
    setRefreshing(true);
    
    try {
      await Promise.all([
        fetchStudentData(true),
        fetchEnrolmentStats(true)
      ]);
      

      const lastSegment = selectedPage.split("/").pop();
      switch (lastSegment) {
        case "attendance":
          await fetchAttendanceData(true);
          break;
        case "progress_check":
          await fetchProgressCheckData(true);
          break;
        case "planpace":
          await fetchPlanPaceData(true);
          break;
        case "checkup":
          await fetchCheckupData(true);
          break;
      }
    } finally {
      setRefreshing(false);
    }
  };

  const clearAllCache = () => {
    Object.keys(CACHE_CONFIG.ENDPOINTS).forEach(endpoint => {
      localStorage.removeItem(`mathnasium_cache_${endpoint}`);
    });
    console.log("All cache cleared");
  };

  useEffect(() => {
    const token = localStorage.getItem("token");
    if (!token) {
      router.push("/");
    } else {
      setIsAuthenticated(true);
      Promise.all([
        fetchStudentData(),
        fetchEnrolmentStats()
      ]).then(() => {
        preloadAllInterventionData();
      });
    }
  }, [router]);

  useEffect(() => {
    if (!isAuthenticated) return;

    const endpointHandlers: Record<string, () => Promise<void>> = {
      "attendance": () => fetchAttendanceData(),
      "progress_check": () => fetchProgressCheckData(),
      "planpace": () => fetchPlanPaceData(),
      "checkup": () => fetchCheckupData()
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
          <div className="ml-auto">
            <Button 
              variant="outline" 
              size="sm"
              onClick={refreshCurrentData}
              disabled={refreshing}
              className="text-white border-white hover:bg-gray-800"
            >
              <RefreshCw className={`h-4 w-4 mr-2 ${refreshing ? 'animate-spin' : ''}`} />
              {refreshing ? 'Refreshing...' : 'Refresh Data'}
            </Button>
          </div>
        </header>
        <div className="flex flex-1 flex-col gap-4 p-4">
          {selectedPage === "/dashboard/general" ? (
            <div className="space-y-6">
              {loading.stats ? (
                <p>Loading stats data...</p>
              ) : statsData.length > 0 ? (
                <SectionCards stats={getExtendedStats()} />
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
              <DataTable columns={planPaceColumns} data={planPaceData} />
            )
          ) : selectedPage === "/dashboard/edu/checkup" ? (
            loading.checkup ? (
              <p>Loading Checkup data...</p>
            ) : (
              <DataTable columns={checkupColumns} data={checkupData} />
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