
"use client";

import * as React from "react";
import { differenceInMonths } from "date-fns";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from "recharts";
import {
  ChartContainer,
  ChartTooltipContent,
  ChartLegendContent,
} from "@/components/ui/chart";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";

export function StudentProgressChart({ data }: { data: any[] }) {
  const [timeFilter, setTimeFilter] = React.useState<string>("all");

  const processData = () => {
    let monthsThreshold: number | undefined;
    
    switch (timeFilter) {
      case "6months": monthsThreshold = 6; break;
      case "1year": monthsThreshold = 12; break;
      case "1.5years": monthsThreshold = 18; break;
      case "2years": monthsThreshold = 24; break;
      default: monthsThreshold = undefined;
    }

    const filteredStudents = monthsThreshold 
      ? data.filter(student => {
          const enrolmentDate = new Date(student.enrolment_start);
          const now = new Date();
          return differenceInMonths(now, enrolmentDate) >= monthsThreshold;
        })
      : data;

    const categories = {
      behind: 0,
      atLevel: 0,
      ahead: 0
    };

    filteredStudents.forEach(student => {
      if (student.assessment_level < student.year) {
        categories.behind++;
      } else if (student.assessment_level === student.year) {
        categories.atLevel++;
      } else {
        categories.ahead++;
      }
    });

    return [
      { name: "Behind", value: categories.behind, color: "#ef4444" },
      { name: "At Level", value: categories.atLevel, color: "#10b981" },
      { name: "Ahead", value: categories.ahead, color: "#f59e0b" },
    ];
  };

  const chartData = processData();

  const chartConfig = {
    behind: { label: "Behind", color: "#ef4444" },
    atLevel: { label: "At Level", color: "#10b981" },
    ahead: { label: "Ahead", color: "#f59e0b" },
  };

  return (
    <Card>
      <CardHeader className="flex flex-row items-center justify-between pb-2">
        <CardTitle className="text-sm font-medium">Student Progress</CardTitle>
        <Select value={timeFilter} onValueChange={setTimeFilter}>
          <SelectTrigger className="w-[180px]">
            <SelectValue placeholder="Filter by enrolment" />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="all">All Students</SelectItem>
            <SelectItem value="6months">6+ Months</SelectItem>
            <SelectItem value="1year">1+ Years</SelectItem>
            <SelectItem value="1.5years">1.5+ Years</SelectItem>
            <SelectItem value="2years">2+ Years</SelectItem>
          </SelectContent>
        </Select>
      </CardHeader>
      <CardContent>
        <ChartContainer config={chartConfig} className="h-[400px]">
          <BarChart data={chartData}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="name" />
            <YAxis />
            <Tooltip 
              content={<ChartTooltipContent />} 
              formatter={(value) => [`${value} students`, ""]}
            />
            <Legend content={<ChartLegendContent />} />
            <Bar 
              dataKey="value" 
              name="Students"
              fill="var(--color)"
              radius={[4, 4, 0, 0]}
            />
          </BarChart>
        </ChartContainer>
      </CardContent>
    </Card>
  );
}