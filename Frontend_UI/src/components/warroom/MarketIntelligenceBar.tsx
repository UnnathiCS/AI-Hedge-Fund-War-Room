import { TrendingUp, TrendingDown, Activity } from "lucide-react";

export interface MarketData {
  name: string;
  ticker: string;
  price: number;
  change: number;
  changePercent: number;
  pe: number;
  volatility: string;
  oneYearReturn: number;
  risk: "low" | "medium" | "high";
  currency?: string;
}

const riskColors = {
  low: "text-neon-green",
  medium: "text-neon-yellow",
  high: "text-neon-red",
};

const riskLabels = {
  low: "LOW RISK",
  medium: "MODERATE",
  high: "HIGH RISK",
};

interface Props {
  data?: MarketData | null;
}

export default function MarketIntelligenceBar({ data }: Props) {
  if (!data) {
    return (
      <div className="glass-card px-6 py-5 flex items-center justify-center">
        <span className="text-sm text-muted-foreground">Select a stock to see market intelligence</span>
      </div>
    );
  }

  const isPositive = data.change >= 0;
  const currencySymbol = data.currency === "INR" ? "₹" : "$";

  return (
    <div className="glass-card px-6 py-3 flex items-center justify-between gap-6 overflow-x-auto">
      <div className="flex items-center gap-4 min-w-fit">
        <div>
          <div className="flex items-center gap-2">
            <span className="text-lg font-bold tracking-tight text-foreground">{data.ticker}</span>
            <span className="text-xs text-muted-foreground">{data.name}</span>
          </div>
          <div className="flex items-center gap-2 mt-0.5">
            <span className="text-2xl font-mono font-bold text-foreground">{currencySymbol}{data.price.toFixed(2)}</span>
            <span className={`flex items-center gap-1 text-sm font-mono font-semibold ${isPositive ? "text-neon-green" : "text-neon-red"}`}>
              {isPositive ? <TrendingUp className="w-3.5 h-3.5" /> : <TrendingDown className="w-3.5 h-3.5" />}
              {isPositive ? "+" : ""}{data.change.toFixed(2)} ({data.changePercent.toFixed(2)}%)
            </span>
          </div>
        </div>
      </div>

      <div className="h-10 w-px bg-border" />

      <div className="flex items-center gap-8 min-w-fit">
        {data.pe > 0 && <MetricItem label="P/E Ratio" value={data.pe.toFixed(1)} />}
        <MetricItem label="Volatility" value={data.volatility} className="text-neon-yellow" />
        <MetricItem
          label="1Y Return"
          value={`${data.oneYearReturn >= 0 ? "+" : ""}${data.oneYearReturn}%`}
          className={data.oneYearReturn >= 0 ? "text-neon-green" : "text-neon-red"}
        />
        <div className="flex flex-col items-center gap-0.5">
          <span className="text-[10px] uppercase tracking-widest text-muted-foreground">Risk</span>
          <div className="flex items-center gap-1.5">
            <Activity className={`w-3.5 h-3.5 ${riskColors[data.risk as keyof typeof riskColors]}`} />
            <span className={`text-sm font-mono font-semibold ${riskColors[data.risk as keyof typeof riskColors]}`}>
              {riskLabels[data.risk as keyof typeof riskLabels]}
            </span>
          </div>
        </div>
      </div>

      <div className="flex items-center gap-2 min-w-fit ml-auto">
        <div className="w-2 h-2 rounded-full bg-neon-green animate-pulse-glow" />
        <span className="text-[10px] uppercase tracking-widest text-neon-green font-mono">LIVE</span>
      </div>
    </div>
  );
}

function MetricItem({ label, value, className = "text-foreground" }: { label: string; value: string; className?: string }) {
  return (
    <div className="flex flex-col items-center gap-0.5">
      <span className="text-[10px] uppercase tracking-widest text-muted-foreground">{label}</span>
      <span className={`text-sm font-mono font-semibold ${className}`}>{value}</span>
    </div>
  );
}
