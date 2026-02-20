import { useParams, useNavigate } from "react-router-dom";
import { mockStudents } from "@/data/students";
import { RiskBadge } from "@/components/RiskBadge";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { ArrowLeft, Mail, BookOpen, BarChart3, Clock, User, Hash } from "lucide-react";

export default function StudentProfile() {
  const { id } = useParams();
  const navigate = useNavigate();
  const student = mockStudents.find((s) => s.id === id);

  if (!student) {
    return (
      <div className="flex flex-col items-center justify-center py-20 text-muted-foreground">
        <p className="text-lg font-medium">Student not found</p>
        <Button variant="outline" className="mt-4" onClick={() => navigate("/dashboard")}>
          <ArrowLeft className="mr-2 h-4 w-4" /> Back to Dashboard
        </Button>
      </div>
    );
  }

  const riskBarColor =
    student.riskLevel === "High"
      ? "bg-risk-high"
      : student.riskLevel === "Medium"
      ? "bg-risk-medium"
      : "bg-risk-low";

  const details = [
    { label: "Student ID", value: student.id, icon: Hash },
    { label: "Email", value: student.email, icon: Mail },
    { label: "Department", value: student.department, icon: BookOpen },
    { label: "Semester", value: student.semester, icon: Clock },
    { label: "GPA", value: student.gpa.toFixed(2), icon: BarChart3 },
    { label: "Attendance", value: `${student.attendance}%`, icon: User },
  ];

  return (
    <div className="space-y-6">
      <div className="flex items-center gap-3">
        <Button variant="ghost" size="icon" onClick={() => navigate(-1)}>
          <ArrowLeft className="h-4 w-4" />
        </Button>
        <div>
          <h1 className="text-2xl font-bold tracking-tight">{student.name}</h1>
          <p className="text-muted-foreground text-sm">Student Profile</p>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Risk Summary */}
        <Card className="lg:col-span-1">
          <CardHeader>
            <CardTitle className="text-base">Risk Assessment</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="text-center space-y-3">
              <RiskBadge level={student.riskLevel} />
              <div>
                <p className="text-4xl font-bold">{student.riskScore}%</p>
                <p className="text-sm text-muted-foreground">Risk Score</p>
              </div>
            </div>
            <div className="h-3 w-full rounded-full bg-muted overflow-hidden">
              <div
                className={`h-full rounded-full transition-all duration-700 ${riskBarColor}`}
                style={{ width: `${student.riskScore}%` }}
              />
            </div>
          </CardContent>
        </Card>

        {/* Details */}
        <Card className="lg:col-span-2">
          <CardHeader>
            <CardTitle className="text-base">Student Details</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              {details.map((d) => (
                <div key={d.label} className="flex items-center gap-3 rounded-lg border p-3">
                  <d.icon className="h-4 w-4 text-muted-foreground shrink-0" />
                  <div>
                    <p className="text-xs text-muted-foreground">{d.label}</p>
                    <p className="text-sm font-medium">{d.value}</p>
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
