import * as React from "react"

import { SearchForm } from "@/components/search-form"
import {
  Sidebar,
  SidebarContent,
  SidebarGroup,
  SidebarGroupContent,
  SidebarGroupLabel,
  SidebarHeader,
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,
} from "@/components/ui/sidebar"


const data = {
  navMain: [
    {
      title: "Home",
      url: "#",
      items: [
        {
          title: "General",
          url: "/dashboard/general",
        },
      ],
    },
    {
      title: "Education Management",
      url: "#",
      items: [
        {
          title: "Progress Check Status",
          url: "/dashboard/edu/progress_check",
        },
        {
          title: "Check-Up Status",
          url: "/dashboard/edu/checkup",
        },
        {
          title: "Plan Pace",
          url: "/dashboard/edu/planpace",
        },
      ],
    },
    {
      title: "At Risk",
      url: "/dashboard/risk",
      items: [
        {
          title: "Attendance",
          url: "/dashboard/risk/attendance",
        }
      ],
    },
  ],
}

export function AppSidebar({
  onSelectPage,
    selectedPage,
  ...props
}: React.ComponentProps<typeof Sidebar> & { onSelectPage: (page: string) => void; selectedPage: string }) {
  return (
    <Sidebar {...props} className="rounded-lg border border-gray-200 shadow-lg">
      <SidebarContent className="py-4">
        {data.navMain.map((item) => (
          <SidebarGroup key={item.title}>
            <SidebarGroupLabel className="text-lg font-medium text-gray-700 mb-2">
              {item.title}
            </SidebarGroupLabel>
            <SidebarGroupContent>
              <SidebarMenu>
                {item.items.map((subItem) => {
                  const isActive = selectedPage === subItem.url
                  return (
                    <SidebarMenuItem key={subItem.title}>
                      <SidebarMenuButton asChild>
                        <a
                          href={subItem.url}
                          onClick={(e) => {
                            e.preventDefault()
                            onSelectPage(subItem.url)
                          }}
                          className={`block py-2 rounded-md text-sm font-medium transition-colors ${
                            isActive ? "bg-red-500 text-white" : "text-gray-700 hover:bg-gray-100"
                          }`}
                        >
                          {subItem.title}
                        </a>
                      </SidebarMenuButton>
                    </SidebarMenuItem>
                  )
                })}
              </SidebarMenu>
            </SidebarGroupContent>
          </SidebarGroup>
        ))}
      </SidebarContent>
    </Sidebar>
  )
}