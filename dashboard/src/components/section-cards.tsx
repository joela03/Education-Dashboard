import { TrendingDownIcon, TrendingUpIcon } from "lucide-react";
import { Badge } from "@/components/ui/badge";
import {
  Card,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
interface SectionCardsProps {
  studentStats?: {
    totalStudents: number;
    enrolled: number;
    onHold: number;
    preEnrolled: number;
  };
  marchStats?: {
    newEnrollments: number;
    avgAttendance: number;
    avgScore: number;
  };
  interventionStats?: {
    needCheckup: number;
    needProgressCheck: number;
    poorAttendance: number;
  };
}

export function SectionCards({
  studentStats,
  marchStats,
  interventionStats
}: SectionCardsProps) {
  return (
    <div className="grid grid-cols-1 gap-4 px-4 lg:grid-cols-3 lg:px-6">
      <Card className="@container/card">
        <CardHeader className="relative">
          <CardDescription>Student Count</CardDescription>
          <CardTitle className="text-2xl font-semibold tabular-nums">
            Total Students: {studentStats?.totalStudents || 0}
          </CardTitle>
        </CardHeader>
        <CardFooter className="flex-col items-start gap-1 text-sm">
          <div className="flex gap-2 font-medium">
            Enroled: {studentStats?.enrolled || 0}
          </div>
          <div className="flex gap-2 text-bold font-medium">
            On-Hold: {studentStats?.onHold || 0}
          </div>
          <div className="flex gap-2 font-medium">
            Pre-Enroled: {studentStats?.preEnrolled || 0}
          </div>
        </CardFooter>
      </Card>
      <Card className="@container/card">
        <CardHeader className="relative">
          <CardDescription>March Stats</CardDescription>
          <CardTitle className="text-2xl font-semibold tabular-nums">
            New enrolments: {marchStats?.newEnrollments || 0}
          </CardTitle>
        </CardHeader>
        <CardFooter className="flex-col items-start gap-1 text-sm">
          <div className="flex gap-2 font-medium">
            Average Attendance: {marchStats?.avgAttendance ? `${marchStats.avgAttendance}%` : '0%'}
          </div>
          <div className="flex gap-2 font-medium">
            Average Score: {marchStats?.avgScore || 0}
          </div>
          <div className="text-muted-foreground"></div>
        </CardFooter>
      </Card>
      <Card className="@container/card">
        <CardHeader className="relative">
          <CardDescription>Education Stats</CardDescription>
          <CardTitle className="text-2xl font-semibold tabular-nums">
            Potential Interventions: 
          </CardTitle>
        </CardHeader>
        <CardFooter className="flex-col items-start gap-1 text-sm">
          <div className="flex gap-2 font-medium">
            Students that need a checkup: {interventionStats?.needCheckup || 0}
          </div>
          <div className="flex gap-2 font-medium">
            Students that need a Progress Check: {interventionStats?.needProgressCheck || 0}
          </div>
          <div className="flex gap-2 font-medium">
            Students with poor attendance: {interventionStats?.poorAttendance || 0}
          </div>
        </CardFooter>
      </Card>
    </div>
  );
}