"use client"

import type { ColumnDef } from "@tanstack/react-table"
import { ArrowUpDown, ExternalLink } from "lucide-react"

import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { formatDate } from "@/lib/utils"

// Define the student data type based on your API response
export type Student = {
  account_link: string
  account_name: string
  attendance_count: number
  enrolment_status: string
  last_attendance: string
  mathnasium_id: number
  name: string
  student_link: string
}

export const columns: ColumnDef<Student>[] = [
  {
    accessorKey: "name",
    header: ({ column }) => {
      return (
        <Button variant="ghost" onClick={() => column.toggleSorting(column.getIsSorted() === "asc")}>
          Student Name
          <ArrowUpDown className="ml-2 h-4 w-4" />
        </Button>
      )
    },
    cell: ({ row }) => {
      const name = row.getValue("name") as string
      const studentLink = row.original.student_link

      return (
        <div className="flex items-center gap-2">
          <a
            href={studentLink}
            target="_blank"
            rel="noopener noreferrer"
            className="font-medium text-primary hover:underline flex items-center gap-1"
          >
            {name}
            <ExternalLink className="h-3 w-3" />
          </a>
        </div>
      )
    },
  },
  {
    accessorKey: "account_name",
    header: ({ column }) => {
      return (
        <Button variant="ghost" onClick={() => column.toggleSorting(column.getIsSorted() === "asc")}>
          Account
          <ArrowUpDown className="ml-2 h-4 w-4" />
        </Button>
      )
    },
    cell: ({ row }) => {
      const accountName = row.getValue("account_name") as string
      const accountLink = row.original.account_link

      return (
        <a
          href={accountLink}
          target="_blank"
          rel="noopener noreferrer"
          className="hover:underline flex items-center gap-1"
        >
          {accountName}
          <ExternalLink className="h-3 w-3" />
        </a>
      )
    },
  },
  {
    accessorKey: "mathnasium_id",
    header: "ID",
    cell: ({ row }) => <div>{row.getValue("mathnasium_id")}</div>,
  },
  {
    accessorKey: "enrolment_status",
    header: "Status",
    cell: ({ row }) => {
      const status = row.getValue("enrolment_status") as string

      return <Badge variant={status === "Enrolment" ? "default" : "secondary"}>{status}</Badge>
    },
  },
  {
    accessorKey: "attendance_count",
    header: ({ column }) => {
      return (
        <Button variant="ghost" onClick={() => column.toggleSorting(column.getIsSorted() === "asc")}>
          Attendance Count
          <ArrowUpDown className="ml-2 h-4 w-4" />
        </Button>
      )
    },
    cell: ({ row }) => <div className="text-center">{row.getValue("attendance_count")}</div>,
  },
  {
    accessorKey: "last_attendance",
    header: ({ column }) => {
      return (
        <Button variant="ghost" onClick={() => column.toggleSorting(column.getIsSorted() === "asc")}>
          Last Attendance
          <ArrowUpDown className="ml-2 h-4 w-4" />
        </Button>
      )
    },
    cell: ({ row }) => {
      const date = row.getValue("last_attendance") as string
      return <div>{formatDate(date)}</div>
    },
  },
]

