import { Info } from "lucide-react";

interface Metric {
  label: string;
  value: number;
  tooltip: string;
  color: string;
}

const metrics: Metric[] = [
  { label: "Analyst Confidence", value: 82, tooltip: "How confident our AI agents are in their analysis based on data quality and coverage.", color: "bg-neon-green" },
  { label: "Bias Index", value: 34, tooltip: "Measures the degree of directional bias. Lower = more neutral analysis.", color: "bg-neon-yellow" },
  { label: "Consensus Strength", value: 67, tooltip: "How much agents agree. Above 70% = strong consensus.", color: "bg-neon-blue" },
  { label: "Disagreement Index", value: 45, tooltip: "Measures how much agents disagree on key points. Higher = more debate.", color: "bg-agent-aggressive" },
];

export default function AnalyticsPanel() {
  return (
    <div className="glass-card p-5 h-full flex flex-col">
      <h3 className="text-xs font-semibold uppercase tracking-widest text-muted-foreground mb-5">Debate Analytics</h3>

      <div className="space-y-5 flex-1">
        {metrics.map((m) => (
          <div key={m.label}>
            <div className="flex items-center justify-between mb-1.5">
              <div className="flex items-center gap-1.5">
                <span className="text-xs font-medium text-foreground">{m.label}</span>
                <div className="group relative">
                  <Info className="w-3 h-3 text-muted-foreground cursor-help" />
                  <div className="absolute bottom-full left-1/2 -translate-x-1/2 mb-2 px-3 py-2 rounded-lg bg-secondary text-xs text-secondary-foreground w-48 opacity-0 group-hover:opacity-100 transition-opacity pointer-events-none z-10">
                    {m.tooltip}
                  </div>
                </div>
              </div>
              <span className="text-xs font-mono font-bold text-foreground">{m.value}%</span>
            </div>
            <div className="h-1.5 rounded-full bg-secondary overflow-hidden">
              <div
                className={`h-full rounded-full ${m.color} transition-all duration-1000 ease-out`}
                style={{ width: `${m.value}%` }}
              />
            </div>
          </div>
        ))}
      </div>

      {/* Sentiment breakdown */}
      <div className="mt-6 pt-5 border-t border-border">
        <h4 className="text-xs font-semibold uppercase tracking-widest text-muted-foreground mb-3">Sentiment Split</h4>
        <div className="flex gap-1 h-3 rounded-full overflow-hidden">
          <div className="bg-neon-green" style={{ width: "55%" }} />
          <div className="bg-neon-yellow" style={{ width: "30%" }} />
          <div className="bg-neon-red" style={{ width: "15%" }} />
        </div>
        <div className="flex justify-between mt-2 text-[10px] text-muted-foreground">
          <span>Bullish 55%</span>
          <span>Neutral 30%</span>
          <span>Bearish 15%</span>
        </div>
      </div>
    </div>
  );
}
