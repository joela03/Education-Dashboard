import { TrendingDownIcon, TrendingUpIcon } from "lucide-react";
import { Badge } from "@/components/ui/badge";
import {
  Card,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";

export function SectionCards() {
  return (
    <div className="grid grid-cols-1 gap-4 px-4 lg:grid-cols-3 lg:px-6">
      <Card className="@container/card">
        <CardHeader className="relative">
          <CardDescription>Student Count</CardDescription>
          <CardTitle className="text-2xl font-semibold tabular-nums">
            Total Students: 
          </CardTitle>
        </CardHeader>
        <CardFooter className="flex-col items-start gap-1 text-sm">
          <div className="flex gap-2 font-medium">
            Enroled:
          </div>
          <div className="flex gap-2 text-bold font-medium">
            On-Hold:
          </div>
          <div className="flex gap-2 font-medium">
            Pre-Enroled:
          </div>
        </CardFooter>
      </Card>
      <Card className="@container/card">
        <CardHeader className="relative">
          <CardDescription>March Stats</CardDescription>
          <CardTitle className="text-2xl font-semibold tabular-nums">
            New enrolments: 
          </CardTitle>
        </CardHeader>
        <CardFooter className="flex-col items-start gap-1 text-sm">
          <div className="flex gap-2 font-medium">
            Average Attendance:
          </div>
          <div className="flex gap-2 font-medium">
            Average Score:
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
            Students that need a checkup
          </div>
          <div className="flex gap-2 font-medium">
            Students that need a Progress Check:
          </div>
          <div className="flex gap-2 font-medium">
            Students with poor attendance 
          </div>
        </CardFooter>
      </Card>
    </div>
  );
}