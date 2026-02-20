import { RiskLevel } from "@/data/students";

const riskStyles: Record<RiskLevel, string> = {
  Low: "bg-risk-low-bg text-risk-low-foreground border border-risk-low/30",
  Medium: "bg-risk-medium-bg text-risk-medium-foreground border border-risk-medium/30",
  High: "bg-risk-high-bg text-risk-high-foreground border border-risk-high/30",
};

export function RiskBadge({ level }: { level: RiskLevel }) {
  return (
    <span className={`inline-flex items-center gap-1.5 rounded-full px-2.5 py-0.5 text-xs font-semibold ${riskStyles[level]}`}>
      <span
        className={`h-1.5 w-1.5 rounded-full ${
          level === "Low" ? "bg-risk-low" : level === "Medium" ? "bg-risk-medium" : "bg-risk-high"
        }`}
      />
      {level}
    </span>
  );
}
