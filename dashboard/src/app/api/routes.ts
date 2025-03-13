import { NextResponse } from "next/server"

export async function GET() {

    const res = await fetch("http://localhost:5000/api/attendance", {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
      },
    });

    if (!res.ok) {
        throw new Error("Failed to fetch students data");
      }

    const students = await res.json();

    return NextResponse.json(students);
}