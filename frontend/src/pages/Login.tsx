import { useState } from "react";
import { GraduationCap, Lock, Mail, ShieldCheck, BookOpen } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Card, CardContent, CardHeader } from "@/components/ui/card";

export type UserRole = "admin" | "faculty";

export default function Login({ onLogin }: { onLogin: (role: UserRole) => void }) {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [role, setRole] = useState<UserRole>("admin");

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onLogin(role);
  };

  return (
    <div className="flex min-h-screen items-center justify-center bg-background px-4">
      <Card className="w-full max-w-md shadow-xl border-border/50">
        <CardHeader className="text-center space-y-4 pb-2">
          <div className="mx-auto flex h-14 w-14 items-center justify-center rounded-2xl bg-primary">
            <GraduationCap className="h-7 w-7 text-primary-foreground" />
          </div>
          <div>
            <h1 className="text-2xl font-bold tracking-tight">ONtrack</h1>
            <p className="text-sm text-muted-foreground mt-1">
              Student Dropout Prediction Dashboard
            </p>
          </div>
        </CardHeader>
        <CardContent className="pt-4">
          <form onSubmit={handleSubmit} className="space-y-4">
            <div className="space-y-2">
              <label className="text-sm font-medium">Email</label>
              <div className="relative">
                <Mail className="absolute left-3 top-2.5 h-4 w-4 text-muted-foreground" />
                <Input
                  type="email"
                  placeholder="admin@university.edu"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  className="pl-10"
                />
              </div>
            </div>
            <div className="space-y-2">
              <label className="text-sm font-medium">Password</label>
              <div className="relative">
                <Lock className="absolute left-3 top-2.5 h-4 w-4 text-muted-foreground" />
                <Input
                  type="password"
                  placeholder="••••••••"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  className="pl-10"
                />
              </div>
            </div>
            <div className="space-y-2">
              <label className="text-sm font-medium">Role</label>
              <div className="grid grid-cols-2 gap-3">
                <button
                  type="button"
                  onClick={() => setRole("admin")}
                  className={`flex flex-col items-center gap-1.5 rounded-lg border-2 p-3 text-sm transition-colors ${
                    role === "admin"
                      ? "border-primary bg-primary/5 text-primary"
                      : "border-border text-muted-foreground hover:border-primary/50"
                  }`}
                >
                  <ShieldCheck className="h-5 w-5" />
                  <span className="font-medium">Admin</span>
                </button>
                <button
                  type="button"
                  onClick={() => setRole("faculty")}
                  className={`flex flex-col items-center gap-1.5 rounded-lg border-2 p-3 text-sm transition-colors ${
                    role === "faculty"
                      ? "border-primary bg-primary/5 text-primary"
                      : "border-border text-muted-foreground hover:border-primary/50"
                  }`}
                >
                  <BookOpen className="h-5 w-5" />
                  <span className="font-medium">Faculty</span>
                </button>
              </div>
            </div>
            <Button type="submit" className="w-full">
              Sign In
            </Button>
            <p className="text-center text-xs text-muted-foreground">
              Demo: select a role and enter any credentials
            </p>
          </form>
        </CardContent>
      </Card>
    </div>
  );
}
