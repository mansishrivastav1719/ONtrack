import { mockStudents, trendData } from "@/data/students";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { PieChart, Pie, Cell, ResponsiveContainer, LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, BarChart, Bar } from "recharts";
import { useMemo } from "react";

const RISK_COLORS = {
  Low: "hsl(142, 71%, 45%)",
  Medium: "hsl(38, 92%, 50%)",
  High: "hsl(0, 84%, 60%)",
};

export default function Reports() {
  const pieData = useMemo(() => {
    const counts = { Low: 0, Medium: 0, High: 0 };
    mockStudents.forEach((s) => counts[s.riskLevel]++);
    return Object.entries(counts).map(([name, value]) => ({ name, value }));
  }, []);

  const deptData = useMemo(() => {
    const map: Record<string, { Low: number; Medium: number; High: number }> = {};
    mockStudents.forEach((s) => {
      if (!map[s.department]) map[s.department] = { Low: 0, Medium: 0, High: 0 };
      map[s.department][s.riskLevel]++;
    });
    return Object.entries(map).map(([dept, counts]) => ({ department: dept, ...counts }));
  }, []);

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold tracking-tight">Reports & Analytics</h1>
        <p className="text-muted-foreground text-sm mt-1">Visual analysis of dropout risk across the institution</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Pie Chart */}
        <Card>
          <CardHeader>
            <CardTitle className="text-base">Risk Distribution</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="h-72">
              <ResponsiveContainer width="100%" height="100%">
                <PieChart>
                  <Pie
                    data={pieData}
                    cx="50%"
                    cy="50%"
                    innerRadius={60}
                    outerRadius={100}
                    paddingAngle={4}
                    dataKey="value"
                    label={({ name, value }) => `${name}: ${value}`}
                  >
                    {pieData.map((entry) => (
                      <Cell key={entry.name} fill={RISK_COLORS[entry.name as keyof typeof RISK_COLORS]} />
                    ))}
                  </Pie>
                  <Tooltip />
                </PieChart>
              </ResponsiveContainer>
            </div>
          </CardContent>
        </Card>

        {/* Line Chart - Trends */}
        <Card>
          <CardHeader>
            <CardTitle className="text-base">Semester-wise Risk Trend</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="h-72">
              <ResponsiveContainer width="100%" height="100%">
                <LineChart data={trendData}>
                  <CartesianGrid strokeDasharray="3 3" stroke="hsl(220, 15%, 90%)" />
                  <XAxis dataKey="semester" tick={{ fontSize: 12 }} />
                  <YAxis tick={{ fontSize: 12 }} />
                  <Tooltip />
                  <Legend />
                  <Line type="monotone" dataKey="low" stroke={RISK_COLORS.Low} strokeWidth={2} name="Low Risk" />
                  <Line type="monotone" dataKey="medium" stroke={RISK_COLORS.Medium} strokeWidth={2} name="Medium Risk" />
                  <Line type="monotone" dataKey="high" stroke={RISK_COLORS.High} strokeWidth={2} name="High Risk" />
                </LineChart>
              </ResponsiveContainer>
            </div>
          </CardContent>
        </Card>

        {/* Bar Chart - Department */}
        <Card className="lg:col-span-2">
          <CardHeader>
            <CardTitle className="text-base">Department-wise Risk Breakdown</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="h-72">
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={deptData}>
                  <CartesianGrid strokeDasharray="3 3" stroke="hsl(220, 15%, 90%)" />
                  <XAxis dataKey="department" tick={{ fontSize: 11 }} />
                  <YAxis tick={{ fontSize: 12 }} />
                  <Tooltip />
                  <Legend />
                  <Bar dataKey="Low" fill={RISK_COLORS.Low} radius={[4, 4, 0, 0]} />
                  <Bar dataKey="Medium" fill={RISK_COLORS.Medium} radius={[4, 4, 0, 0]} />
                  <Bar dataKey="High" fill={RISK_COLORS.High} radius={[4, 4, 0, 0]} />
                </BarChart>
              </ResponsiveContainer>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
