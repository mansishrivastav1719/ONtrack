import { ReactNode } from "react";
import { AppSidebar } from "@/components/AppSidebar";
import type { UserRole } from "@/pages/Login";

export function DashboardLayout({
  children,
  onLogout,
  role,
}: {
  children: ReactNode;
  onLogout: () => void;
  role: UserRole;
}) {
  return (
    <div className="flex min-h-screen w-full bg-background">
      <AppSidebar onLogout={onLogout} role={role} />
      <main className="flex-1 overflow-auto">
        <div className="p-6 lg:p-8">{children}</div>
      </main>
    </div>
  );
}
