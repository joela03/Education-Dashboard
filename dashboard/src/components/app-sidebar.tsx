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
  SidebarRail,
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
          isActive: true,
        }
      ],
    },
  ],
}

export function AppSidebar({
  onSelectPage,
  ...props
}: React.ComponentProps<typeof Sidebar> & { onSelectPage: (page: string) => void }) {
  return (
    <Sidebar {...props}>
      <SidebarHeader>
        <SearchForm />
      </SidebarHeader>
      <SidebarContent>
        {data.navMain.map((item) => (
          <SidebarGroup key={item.title}>
            <SidebarGroupLabel>{item.title}</SidebarGroupLabel>
            <SidebarGroupContent>
              <SidebarMenu>
                {item.items.map((subItem) => (
                  <SidebarMenuItem key={subItem.title}>
                    <SidebarMenuButton asChild isActive={subItem.isActive ?? false}>
                      <a
                        href={subItem.url}
                        onClick={(e) => {
                          e.preventDefault()
                          onSelectPage(subItem.url)
                        }}
                      >
                        {subItem.title}
                      </a>
                    </SidebarMenuButton>
                  </SidebarMenuItem>
                ))}
              </SidebarMenu>
            </SidebarGroupContent>
          </SidebarGroup>
        ))}
      </SidebarContent>
      <SidebarRail />
    </Sidebar>
  )
}
