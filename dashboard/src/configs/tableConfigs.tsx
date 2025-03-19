"use client"

import dayjs from "dayjs";
import React from "react";
import { ColumnDef} from "@tanstack/react-table"
import { Button } from "@/components/ui/button";
import { MdArrowUpward, MdArrowDownward } from "react-icons/md";


const parseDate = (date: string | Date) => {
  const parsedDate = new Date(date);
  return parsedDate.toLocaleDateString('en-UK', {
    day: 'numeric',
    year: 'numeric',
    month: 'short',
  });
};

const SortingHeader = ({
  column,
  label,
}: {
  column: any;
  label: string;
}) => {
  const isSortedAsc = column.getIsSorted() === "asc";
  const isSortedDesc = column.getIsSorted() === "desc";

  return (
    <Button
      variant="ghost"
      onClick={() => column.toggleSorting(column.getIsSorted() === "asc")}
      aria-label={`Sort by ${label}`}
    >
      {label}
      {isSortedAsc ? (
        <MdArrowUpward className="ml-2 h-4 w-4" />
      ) : isSortedDesc ? (
        <MdArrowDownward className="ml-2 h-4 w-4" />
      ) : (
        <MdArrowUpward className="ml-2 h-4 w-4" />
      )}
    </Button>
  );
};


const timeSinceDate = (date: Date, period: "day" | "week" | "month"): number => {
  return dayjs().diff(dayjs(date), period, true);
};

export type AttendanceData = {
  name: string
  mathnasium_id: string
  account_name: string
  attendance_count: number
  last_attendance: string
  enrolment_status: string
  account_link: string
  student_link: string
}

export type ProgressCheckData = {
  name: string
  mathnasium_id: string
  student_link: string
  enrolment_status: string
  skills_mastered_percent: Float16Array
  last_assessment: Date
  last_progress_check: Date
  months_since_last_assessment: Date
}

export type PlanPaceData = {
  name: string
  mathnasium_id: string
  student_link: string
  enrolment_status: string
  skills_mastered_percent: Float16Array
  last_assessment: Date
  weeks_since_last_assessment: BigInteger
  expected_plan_percentage: string
}

export type CheckupData = {
  name: string
  mathnasium_id: string
  student_link: string
  enrolment_status: string
  skills_mastered_percent: Float16Array
  last_assessment: Date
  months_since_last_assessment: BigInteger
}

export const attendanceColumns: ColumnDef<AttendanceData>[] = [
  {
    accessorKey: "name",
    header: "Student Name",
    cell: ({ row }) => {
        const name = row.original.name;
        const studentLink = row.original.student_link;
    
        return (
            <a href={studentLink} className="text-blue-500 hover:underline" target="_blank" rel="noopener noreferrer">
                {name}
            </a>
        );
    },
  },
  {
    accessorKey: "mathnasium_id",
    header: "Mathnasium ID",
  },
  {
    accessorKey: "attendance_count",
    header: ({ column }) => <SortingHeader column={column} label="ATTENDANCE COUNT" />,
  },
  {
    accessorKey: "last_attendance",
    header: ({ column }) => <SortingHeader column={column} label="LAST ATTENDANCE" />,
    accessorFn: (row) => new Date(row.last_attendance),
    cell: ({ row }) => {
      const lastAttendanceDate = row.original.last_attendance;
      return <span>{parseDate(lastAttendanceDate)}</span>;
    }
  },
  {
    accessorKey: "enrolment_status",
    header: "Enrolment Status",
  },
  {
    accessorKey: "account_name",
    header: "Account Name",
    cell: ({ row }) => {
      const accountName = row.original.account_name;
      const accountLink = row.original.account_link;

      return (
        <a href={accountLink} className="text-blue-500 hover:underline" target="_blank" rel="noopener noreferrer">
          {accountName}
        </a>
      );
    },
  },
];

export const progressCheckColumns: ColumnDef<ProgressCheckData>[] = [
  {
    accessorKey: "name",
    header: "Student Name",
    cell: ({ row }) => {
        const name = row.original.name;
        const studentLink = row.original.student_link;
    
        return (
            <a href={studentLink} className="text-blue-500 hover:underline" target="_blank" rel="noopener noreferrer">
                {name}
            </a>
        );
    },
  },
  {
    accessorKey: "mathnasium_id",
    header: "Mathnasium ID",
  },
  {
    accessorKey: "skills_mastered_percent",
    header: ({ column }) => <SortingHeader column={column} label="SKILLS MASTERED PERCENT" />,
  },
  {
    accessorKey: "last_assessment",
    header: ({ column }) => <SortingHeader column={column} label="LAST ASSESSMENT" />,
    accessorFn: (row) => new Date(row.last_assessment),
    cell: ({ row }) => {
      const lastAssessment = row.original.last_assessment;
      return <span>{parseDate(lastAssessment)}</span>;
    }
  },
  {
    accessorKey: "months_since_last_assessment",
    header: ({ column }) => <SortingHeader column={column} label="MONTHS SINCE LAST ASSESSMENT" />,
    accessorFn: (row) => timeSinceDate(row.last_assessment, "month"),
    cell: ({ row }) => {
      const lastAssessment = row.original.last_assessment;
      const monthsSinceLastAssessment = timeSinceDate(lastAssessment, "month");

      return <span>{monthsSinceLastAssessment.toFixed(1)}</span>; 
    }
  },
  {
    accessorKey: "last_progress_check",
    header: ({ column }) => <SortingHeader column={column} label="LAST PROGRESS CHECK" />,
    accessorFn: (row) => new Date(row.last_progress_check),
    cell: ({ row }) => {
      const lastProgressCheck = row.original.last_progress_check;
      return <span>{parseDate(lastProgressCheck)}</span>;
    }
  },
];

export const checkupColumns: ColumnDef<CheckupData>[] = [
  {
    accessorKey: "name",
    header: "Student Name",
    cell: ({ row }) => {
        const name = row.original.name;
        const studentLink = row.original.student_link;
    
        return (
            <a href={studentLink} className="text-blue-500 hover:underline" target="_blank" rel="noopener noreferrer">
                {name}
            </a>
        );
    },
  },
  {
    accessorKey: "mathnasium_id",
    header: "Mathnasium ID",
  },
  {
    accessorKey: "skills_mastered_percent",
    header: ({ column }) => <SortingHeader column={column} label="SKILLS MASTERED PERCENT" />,
  },
  {
    accessorKey: "last_assessment",
    header: "Last Assessment",
    cell: ({ row }) => {
      const lastAssessment = row.original.last_assessment;
      return <span>{parseDate(lastAssessment)}</span>;
    }
  },
  {
    accessorKey: "months_since_assessment",
    header: "Months Since Last Assessment",
    cell: ({ row }) => {
      const lastAssessment = row.original.last_assessment;
      return <span>{timeSinceDate(lastAssessment, "month").toFixed(1)}</span>;
    }
  },
];

export const planPaceColumns: ColumnDef<PlanPaceData>[] = [
  {
    accessorKey: "name",
    header: "Student Name",
    cell: ({ row }) => {
        const name = row.original.name;
        const studentLink = row.original.student_link;
    
        return (
            <a href={studentLink} className="text-blue-500 hover:underline" target="_blank" rel="noopener noreferrer">
                {name}
            </a>
        );
    },
  },
  {
    accessorKey: "mathnasium_id",
    header: "Mathnasium ID",
  },
  {
    accessorKey: "skills_mastered_percent",
    header: ({ column }) => <SortingHeader column={column} label="SKILLS MASTERED PERCENT" />,
  },
  {
    accessorKey: "expected_plan_percentage",
    header: ({ column }) => <SortingHeader column={column} label="EXPECTED PLAN PERCENT" />,
    accessorFn: (row) => timeSinceDate(row.last_assessment, "week"),
    cell: ({ row }) => {
      const lastAssessment = row.original.last_assessment;
      return <span>{(timeSinceDate(lastAssessment, "week")*4).toFixed(1)}</span>;
    }
  },
  {
    accessorKey: "last_assessment",
    header: ({ column }) => <SortingHeader column={column} label="LAST ASSESSMENT" />,
    accessorFn: (row) => new Date(row.last_assessment),
    cell: ({ row }) => {
      const lastAssessment = row.original.last_assessment;
      return <span>{parseDate(lastAssessment)}</span>;
    }
  },
  {
    accessorKey: "months_since_last_assessment",
    header: ({ column }) => <SortingHeader column={column} label="MONTHS SINCE LAST ASSESSMENT" />,
    accessorFn: (row) => timeSinceDate(row.last_assessment, "month"),
    cell: ({ row }) => {
      const lastAssessment = row.original.last_assessment;
      const monthsSinceLastAssessment = timeSinceDate(lastAssessment, "month");

      return <span>{monthsSinceLastAssessment.toFixed(1)}</span>; 
    }
  },
];