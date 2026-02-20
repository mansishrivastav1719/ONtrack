import { useState, useMemo } from "react";
import { useNavigate } from "react-router-dom";
import { mockStudents } from "@/data/students";
import { RiskBadge } from "@/components/RiskBadge";
import { Input } from "@/components/ui/input";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Users, AlertTriangle, TrendingDown, GraduationCap, Search } from "lucide-react";

export default function Dashboard() {
  const navigate = useNavigate();
  const [search, setSearch] = useState("");
  const [riskFilter, setRiskFilter] = useState("all");
  const [semFilter, setSemFilter] = useState("all");

  const filtered = useMemo(() => {
    return mockStudents.filter((s) => {
      const matchSearch =
        s.name.toLowerCase().includes(search.toLowerCase()) ||
        s.id.toLowerCase().includes(search.toLowerCase());
      const matchRisk = riskFilter === "all" || s.riskLevel === riskFilter;
      const matchSem = semFilter === "all" || s.semester.toString() === semFilter;
      return matchSearch && matchRisk && matchSem;
    });
  }, [search, riskFilter, semFilter]);

  const stats = useMemo(() => {
    const total = mockStudents.length;
    const high = mockStudents.filter((s) => s.riskLevel === "High").length;
    const medium = mockStudents.filter((s) => s.riskLevel === "Medium").length;
    const avgGpa = (mockStudents.reduce((a, s) => a + s.gpa, 0) / total).toFixed(2);
    return { total, high, medium, avgGpa };
  }, []);

  const statCards = [
    { label: "Total Students", value: stats.total, icon: Users, color: "text-primary" },
    { label: "High Risk", value: stats.high, icon: AlertTriangle, color: "text-risk-high" },
    { label: "Medium Risk", value: stats.medium, icon: TrendingDown, color: "text-risk-medium" },
    { label: "Avg GPA", value: stats.avgGpa, icon: GraduationCap, color: "text-risk-low" },
  ];

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold tracking-tight">Dashboard</h1>
        <p className="text-muted-foreground text-sm mt-1">Overview of student dropout risk analysis</p>
      </div>

      {/* Stat Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        {statCards.map((s) => (
          <Card key={s.label}>
            <CardContent className="flex items-center gap-4 p-5">
              <div className={`flex h-10 w-10 items-center justify-center rounded-xl bg-muted ${s.color}`}>
                <s.icon className="h-5 w-5" />
              </div>
              <div>
                <p className="text-2xl font-bold">{s.value}</p>
                <p className="text-xs text-muted-foreground">{s.label}</p>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>

      {/* Filters */}
      <Card>
        <CardHeader className="pb-3">
          <CardTitle className="text-base">Student Records</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="flex flex-col sm:flex-row gap-3 mb-4">
            <div className="relative flex-1">
              <Search className="absolute left-3 top-2.5 h-4 w-4 text-muted-foreground" />
              <Input
                placeholder="Search by name or ID..."
                value={search}
                onChange={(e) => setSearch(e.target.value)}
                className="pl-10"
              />
            </div>
            <Select value={riskFilter} onValueChange={setRiskFilter}>
              <SelectTrigger className="w-full sm:w-40">
                <SelectValue placeholder="Risk Level" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="all">All Risks</SelectItem>
                <SelectItem value="Low">Low</SelectItem>
                <SelectItem value="Medium">Medium</SelectItem>
                <SelectItem value="High">High</SelectItem>
              </SelectContent>
            </Select>
            <Select value={semFilter} onValueChange={setSemFilter}>
              <SelectTrigger className="w-full sm:w-40">
                <SelectValue placeholder="Semester" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="all">All Semesters</SelectItem>
                {[1, 2, 3, 4, 5, 6, 7, 8].map((s) => (
                  <SelectItem key={s} value={s.toString()}>Semester {s}</SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>

          {/* Table */}
          <div className="overflow-x-auto rounded-lg border border-border">
            <table className="w-full text-sm">
              <thead>
                <tr className="border-b bg-muted/50">
                  <th className="px-4 py-3 text-left font-medium text-muted-foreground">Name</th>
                  <th className="px-4 py-3 text-left font-medium text-muted-foreground">ID</th>
                  <th className="px-4 py-3 text-left font-medium text-muted-foreground">Semester</th>
                  <th className="px-4 py-3 text-left font-medium text-muted-foreground">GPA</th>
                  <th className="px-4 py-3 text-left font-medium text-muted-foreground">Attendance</th>
                  <th className="px-4 py-3 text-left font-medium text-muted-foreground">Risk Level</th>
                </tr>
              </thead>
              <tbody>
                {filtered.map((s) => (
                  <tr key={s.id} className="border-b last:border-0 hover:bg-muted/30 transition-colors cursor-pointer" onClick={() => navigate(`/student/${s.id}`)}>
                    <td className="px-4 py-3 font-medium text-primary hover:underline">{s.name}</td>
                    <td className="px-4 py-3 text-muted-foreground">{s.id}</td>
                    <td className="px-4 py-3">{s.semester}</td>
                    <td className="px-4 py-3">{s.gpa.toFixed(1)}</td>
                    <td className="px-4 py-3">{s.attendance}%</td>
                    <td className="px-4 py-3"><RiskBadge level={s.riskLevel} /></td>
                  </tr>
                ))}
                {filtered.length === 0 && (
                  <tr>
                    <td colSpan={6} className="px-4 py-8 text-center text-muted-foreground">
                      No students found matching your criteria.
                    </td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
