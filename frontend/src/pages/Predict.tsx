import { useState } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { RiskBadge } from "@/components/RiskBadge";
import { BrainCircuit, BarChart3, TrendingUp, BookOpen, Clock } from "lucide-react";
import type { RiskLevel } from "@/data/students";

interface PredictionResult {
  riskLevel: RiskLevel;
  probability: number;
  factors: { name: string; impact: string; icon: React.ElementType }[];
}

function getPrediction(gpa: number, attendance: number): PredictionResult {
  const score = (4.0 - gpa) * 15 + (100 - attendance) * 0.6;
  const probability = Math.min(Math.max(Math.round(score), 2), 98);
  const riskLevel: RiskLevel = probability >= 65 ? "High" : probability >= 35 ? "Medium" : "Low";

  const factors = [
    { name: "GPA Impact", impact: gpa < 2.5 ? "Strong negative" : gpa < 3.0 ? "Moderate" : "Positive", icon: BookOpen },
    { name: "Attendance Impact", impact: attendance < 60 ? "Strong negative" : attendance < 75 ? "Moderate" : "Positive", icon: Clock },
    { name: "Overall Trend", impact: probability >= 65 ? "Declining" : probability >= 35 ? "Stable" : "Improving", icon: TrendingUp },
  ];

  return { riskLevel, probability, factors };
}

export default function Predict() {
  const [studentId, setStudentId] = useState("");
  const [semester, setSemester] = useState("");
  const [gpa, setGpa] = useState("");
  const [attendance, setAttendance] = useState("");
  const [result, setResult] = useState<PredictionResult | null>(null);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    const prediction = getPrediction(parseFloat(gpa) || 2.5, parseFloat(attendance) || 70);
    setResult(prediction);
  };

  const riskBarColor =
    result?.riskLevel === "High"
      ? "bg-risk-high"
      : result?.riskLevel === "Medium"
      ? "bg-risk-medium"
      : "bg-risk-low";

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold tracking-tight">Predict Student Risk</h1>
        <p className="text-muted-foreground text-sm mt-1">Enter student details to predict dropout risk</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Form */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2 text-base">
              <BrainCircuit className="h-4 w-4" /> Input Student Data
            </CardTitle>
          </CardHeader>
          <CardContent>
            <form onSubmit={handleSubmit} className="space-y-4">
              <div className="space-y-2">
                <label className="text-sm font-medium">Student ID</label>
                <Input placeholder="e.g. STU016" value={studentId} onChange={(e) => setStudentId(e.target.value)} />
              </div>
              <div className="space-y-2">
                <label className="text-sm font-medium">Semester</label>
                <Input type="number" placeholder="e.g. 4" min={1} max={8} value={semester} onChange={(e) => setSemester(e.target.value)} />
              </div>
              <div className="space-y-2">
                <label className="text-sm font-medium">GPA (0.0 - 4.0)</label>
                <Input type="number" step="0.1" placeholder="e.g. 2.8" min={0} max={4} value={gpa} onChange={(e) => setGpa(e.target.value)} />
              </div>
              <div className="space-y-2">
                <label className="text-sm font-medium">Attendance (%)</label>
                <Input type="number" placeholder="e.g. 72" min={0} max={100} value={attendance} onChange={(e) => setAttendance(e.target.value)} />
              </div>
              <Button type="submit" className="w-full">
                <BrainCircuit className="mr-2 h-4 w-4" />
                Get Prediction
              </Button>
            </form>
          </CardContent>
        </Card>

        {/* Result */}
        <Card className={result ? "border-border" : "border-dashed border-border/50"}>
          <CardHeader>
            <CardTitle className="flex items-center gap-2 text-base">
              <BarChart3 className="h-4 w-4" /> Prediction Result
            </CardTitle>
          </CardHeader>
          <CardContent>
            {!result ? (
              <div className="flex flex-col items-center justify-center py-12 text-muted-foreground">
                <BrainCircuit className="h-12 w-12 mb-3 opacity-30" />
                <p className="text-sm">Submit student data to see prediction</p>
              </div>
            ) : (
              <div className="space-y-6">
                <div className="text-center space-y-3">
                  <RiskBadge level={result.riskLevel} />
                  <div>
                    <p className="text-4xl font-bold">{result.probability}%</p>
                    <p className="text-sm text-muted-foreground">Dropout Probability</p>
                  </div>
                </div>

                {/* Progress bar */}
                <div className="h-3 w-full rounded-full bg-muted overflow-hidden">
                  <div
                    className={`h-full rounded-full transition-all duration-700 ${riskBarColor}`}
                    style={{ width: `${result.probability}%` }}
                  />
                </div>

                {/* Factors */}
                <div className="space-y-3">
                  <h4 className="text-sm font-medium">Contributing Factors</h4>
                  {result.factors.map((f) => (
                    <div key={f.name} className="flex items-center gap-3 rounded-lg border p-3">
                      <f.icon className="h-4 w-4 text-muted-foreground shrink-0" />
                      <div className="flex-1">
                        <p className="text-sm font-medium">{f.name}</p>
                        <p className="text-xs text-muted-foreground">{f.impact}</p>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
