import { useState } from "react";
import { toast } from "sonner";
import MarketIntelligenceBar, { type MarketData } from "@/components/warroom/MarketIntelligenceBar";
import DebateRoom from "@/components/warroom/DebateRoom";
import AnalyticsPanel from "@/components/warroom/AnalyticsPanel";
import FinalVerdict from "@/components/warroom/FinalVerdict";
import BeginnerMode from "@/components/warroom/BeginnerMode";
import StockSelector from "@/components/warroom/StockSelector";
import UserProfile, { type UserInfo } from "@/components/warroom/UserProfile";
import { convertBackendMessages, type DebateMessage } from "@/components/warroom/debateData";
import { runDebate } from "@/services/backendApi";
import { supabase } from "@/integrations/supabase/client";

export default function Index() {
  const [marketData, setMarketData] = useState<MarketData | null>(null);
  const [debateMessages, setDebateMessages] = useState<DebateMessage[]>([]);
  const [isDebating, setIsDebating] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [currentBroker, setCurrentBroker] = useState("");
  const [currentStock, setCurrentStock] = useState("");
  const [userInfo, setUserInfo] = useState<UserInfo>({ name: "", gender: "male", expertise: "beginner" });

  const handleStart = async (broker: string, ticker: string, companyName: string) => {
    setIsLoading(true);
    setIsDebating(false);
    setDebateMessages([]);
    setCurrentBroker(broker);
    setCurrentStock(companyName);

    try {
      // Run debate and get data from Python backend, passing user info
      const response = await runDebate(companyName, ticker, userInfo);

      // Transform backend market data to frontend format
      const md: MarketData = {
        name: companyName,
        ticker: ticker,
        price: response.market_data.current_price,
        change: 0, // Backend doesn't provide, can be added
        changePercent: response.market_data.one_year_return,
        pe: response.market_data.pe_ratio,
        volatility: response.market_data.volatility.toString(), // Convert to string
        oneYearReturn: response.market_data.one_year_return,
        risk: response.market_data.volatility > 0.3 ? "high" : response.market_data.volatility > 0.15 ? "medium" : "low",
        currency: "INR",
      };

      setMarketData(md);

      // Convert backend debate messages to frontend format
      const msgs: DebateMessage[] = convertBackendMessages(response.debate_messages);
      setDebateMessages(msgs);
      setIsDebating(true);

      // Store in database
      const verdict = "BUY"; // Default, will be recalculated in FinalVerdict
      await supabase.from("debate_sessions").insert({
        broker,
        ticker: md.ticker,
        company_name: md.name,
        stock_price: md.price,
        pe_ratio: md.pe,
        change_percent: md.changePercent,
        verdict,
        debate_messages: msgs as any,
        analytics: {
          volatility: md.volatility,
          risk: md.risk,
          oneYearReturn: md.oneYearReturn,
        } as any,
      });

      toast.success(`Debate started for ${md.name} via ${broker}`);
    } catch (err: any) {
      console.error("Error:", err);
      toast.error(err.message || "Failed to run debate. Make sure the backend is running on localhost:8501");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-background p-4 flex flex-col gap-4 max-w-[1600px] mx-auto">
      {/* Title */}
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-3">
          <h1 className="text-lg font-bold tracking-tight text-foreground">AI Hedge Fund War Room</h1>
          <span className="text-[10px] font-mono uppercase tracking-widest text-muted-foreground px-2 py-0.5 rounded bg-secondary">Beta</span>
        </div>
        <span className="text-[10px] font-mono text-muted-foreground">SESSION #{Math.floor(Math.random() * 99999)} • {new Date().toLocaleDateString("en-IN", { month: "short", day: "numeric", year: "numeric" }).toUpperCase()}</span>
      </div>

      {/* User Profile */}
      <UserProfile onUserInfoChange={setUserInfo} isDisabled={isDebating} />

      {/* Stock Selector */}
      <StockSelector onStart={handleStart} isLoading={isLoading} />

      {/* Market Bar */}
      <MarketIntelligenceBar data={marketData} />

      {/* Main Content: Debate + Analytics */}
      <div className="flex-1 grid grid-cols-1 lg:grid-cols-[1fr_320px] gap-4 min-h-[500px]">
        <DebateRoom messages={debateMessages} isActive={isDebating} />
        <AnalyticsPanel />
      </div>

      {/* Bottom */}
      <FinalVerdict messages={debateMessages} userName={userInfo.name || "Trader"} userExpertise={userInfo.expertise} />
      <BeginnerMode stockName={currentStock} messages={debateMessages} />
    </div>
  );
}
