import { NextResponse } from "next/server"

export async function GET() {

    const res = await fetch("http://localhost:5000/api/students", {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
      },
    });

    const students = await res.json();

    return NextResponse.json(students);
}