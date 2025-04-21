import {
  Card,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";

interface ExtendedStatsProps {
  active_enrolment: number;
  avg_attendance: string;
  on_hold: number;
  pre_enroled: number;
  previous_month_enrolments: number;
  needCheckup?: number;
  needProgressCheck?: number;
  poorAttendance?: number;
}

interface SectionCardsProps {
  stats?: ExtendedStatsProps;
}

export function SectionCards({ stats }: SectionCardsProps) {
  const totalStudents = (stats?.active_enrolment || 0) + 
                       (stats?.on_hold || 0) + 
                       (stats?.pre_enroled || 0);                    
  
  const totalInterventions = (stats?.needCheckup || 0) + 
  (stats?.needProgressCheck || 0) + 
  (stats?.poorAttendance || 0);        

  return (
    <div className="grid grid-cols-1 gap-4 px-4 lg:grid-cols-3 lg:px-6">
      <Card className="@container/card">
        <CardHeader className="relative">
          <CardDescription>Student Count</CardDescription>
          <CardTitle className="text-2xl font-semibold tabular-nums">
            Total Students: {totalStudents}
          </CardTitle>
        </CardHeader>
        <CardFooter className="flex-col items-start gap-1 text-sm">
          <div className="flex gap-2 font-medium">
            Enrolled: {stats?.active_enrolment || 0}
          </div>
          <div className="flex gap-2 font-medium">
            On-Hold: {stats?.on_hold || 0}
          </div>
          <div className="flex gap-2 font-medium">
            Pre-Enrolled: {stats?.pre_enroled || 0}
          </div>
        </CardFooter>
      </Card>

      <Card className="@container/card">
        <CardHeader className="relative">
          <CardDescription>Monthly Stats</CardDescription>
          <CardTitle className="text-2xl font-semibold tabular-nums">
            New Enrollments: {stats?.previous_month_enrolments || 0}
          </CardTitle>
        </CardHeader>
        <CardFooter className="flex-col items-start gap-1 text-sm">
          <div className="flex gap-2 font-medium">
            Average Attendance: {stats?.avg_attendance ? `${parseFloat(stats.avg_attendance).toFixed(1)} sessions` : '0 sessions'}
          </div>
        </CardFooter>
      </Card>

      <Card className="@container/card">
        <CardHeader className="relative">
          <CardDescription>Education Stats</CardDescription>
          <CardTitle className="text-2xl font-semibold tabular-nums">
            Potential Interventions: {totalInterventions}
          </CardTitle>
        </CardHeader>
        <CardFooter className="flex-col items-start gap-1 text-sm">
          <div className="flex gap-2 font-medium">
            Students that need a Checkup: {stats?.needCheckup || 0}
          </div>
          <div className="flex gap-2 font-medium">
            Students that need a Progress Check: {stats?.needProgressCheck || 0}
          </div>
          <div className="flex gap-2 font-medium">
            Students with Poor Attendance: {stats?.poorAttendance || 0}
          </div>
        </CardFooter>
      </Card>
    </div>
  );
}