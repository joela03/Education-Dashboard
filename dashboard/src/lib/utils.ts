import { clsx, type ClassValue } from "clsx"
import { twMerge } from "tailwind-merge"
import { differenceInMonths } from "date-fns";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}

export function formatDate(dateString: string): string {
  if (!dateString) return "N/A"

  try {
    const date = new Date(dateString)
    return new Intl.DateTimeFormat("en-US", {
      year: "numeric",
      month: "short",
      day: "numeric",
    }).format(date)
  } catch (error) {
    return dateString
  }
}

export function categoriseStudents(students: any[], monthsThreshold?: number) {
  const now = new Date();
  
  const filteredStudents = monthsThreshold 
    ? students.filter(student => {
        const enrolmentDate = new Date(student.enrolment_start);
        return differenceInMonths(now, enrolmentDate) >= monthsThreshold;
      })
    : students;

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

  return categories;
}