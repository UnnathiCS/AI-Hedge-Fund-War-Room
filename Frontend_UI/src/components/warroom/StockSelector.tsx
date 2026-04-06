import { useState } from "react";
import { Play, Search } from "lucide-react";
import { INDIAN_BROKERS, POPULAR_STOCKS } from "./debateData";

interface StockSelectorProps {
  onStart: (broker: string, ticker: string, companyName: string) => void;
  isLoading: boolean;
}

export default function StockSelector({ onStart, isLoading }: StockSelectorProps) {
  const [broker, setBroker] = useState(INDIAN_BROKERS[0]);
  const [selectedStock, setSelectedStock] = useState("");
  const [search, setSearch] = useState("");

  const filteredStocks = POPULAR_STOCKS.filter(
    (s) =>
      s.name.toLowerCase().includes(search.toLowerCase()) ||
      s.ticker.toLowerCase().includes(search.toLowerCase())
  );

  const selected = POPULAR_STOCKS.find((s) => s.ticker === selectedStock);

  const handleStart = () => {
    if (!selectedStock || !broker) return;
    const stock = POPULAR_STOCKS.find((s) => s.ticker === selectedStock);
    if (stock) onStart(broker, stock.ticker, stock.name);
  };

  return (
    <div className="glass-card px-5 py-4">
      <div className="flex flex-wrap items-end gap-4">
        {/* Broker */}
        <div className="flex flex-col gap-1.5 min-w-[180px]">
          <label className="text-[10px] uppercase tracking-widest text-muted-foreground font-semibold">Broker</label>
          <select
            value={broker}
            onChange={(e) => setBroker(e.target.value)}
            className="h-9 rounded-lg bg-secondary text-foreground text-sm px-3 border border-border focus:border-neon-green focus:outline-none transition-colors"
          >
            {INDIAN_BROKERS.map((b) => (
              <option key={b} value={b}>{b}</option>
            ))}
          </select>
        </div>

        {/* Company */}
        <div className="flex flex-col gap-1.5 flex-1 min-w-[250px]">
          <label className="text-[10px] uppercase tracking-widest text-muted-foreground font-semibold">Company</label>
          <div className="relative">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-3.5 h-3.5 text-muted-foreground" />
            <select
              value={selectedStock}
              onChange={(e) => setSelectedStock(e.target.value)}
              className="h-9 w-full rounded-lg bg-secondary text-foreground text-sm pl-9 pr-3 border border-border focus:border-neon-green focus:outline-none transition-colors"
            >
              <option value="">Select a company...</option>
              {POPULAR_STOCKS.map((s) => (
                <option key={s.ticker} value={s.ticker}>
                  {s.name} ({s.ticker})
                </option>
              ))}
            </select>
          </div>
        </div>

        {/* Start button */}
        <button
          onClick={handleStart}
          disabled={!selectedStock || isLoading}
          className="h-9 px-6 rounded-lg bg-neon-green text-background font-semibold text-sm flex items-center gap-2 hover:bg-neon-green/90 transition-colors disabled:opacity-40 disabled:cursor-not-allowed"
        >
          {isLoading ? (
            <>
              <div className="w-4 h-4 border-2 border-background/30 border-t-background rounded-full animate-spin" />
              Loading...
            </>
          ) : (
            <>
              <Play className="w-4 h-4" />
              Start Debate
            </>
          )}
        </button>
      </div>

      {selected && (
        <div className="mt-2 text-xs text-muted-foreground">
          Ready to analyze <span className="text-foreground font-medium">{selected.name}</span> via <span className="text-neon-green font-medium">{broker}</span>
        </div>
      )}
    </div>
  );
}
