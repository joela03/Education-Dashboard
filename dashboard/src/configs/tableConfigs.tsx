"use client"
import React from "react";
import { ColumnDef } from "@tanstack/react-table"

const parseDate = (date: string | Date) => {
  const parsedDate = new Date(date);
  return parsedDate.toLocaleDateString('en-US', {
    weekday: 'short',
    day: 'numeric',
    year: 'numeric',
    month: 'short',
  });
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
  skills_masteres_percent: Float16Array
  last_assessment: Date
  last_progress_check: Date
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
    header: "Attendance Count",
  },
  {
    accessorKey: "last_attendance",
    header: "Last Attendance",
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
    header: "Skills Mastered Percent",
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
    accessorKey: "last_progress_check",
    header: "Last Progress Check",
    cell: ({ row }) => {
      const lastProgressCheck = row.original.last_progress_check;
      return <span>{parseDate(lastProgressCheck)}</span>;
    }
  },
];