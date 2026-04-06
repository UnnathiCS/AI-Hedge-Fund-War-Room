import { agents, type DebateMessage } from "./debateData";
import AgentAvatar from "./AgentAvatar";

const voteStyle = {
  BUY: "text-neon-green border-neon-green/30 bg-neon-green/10",
  HOLD: "text-neon-yellow border-neon-yellow/30 bg-neon-yellow/10",
  AVOID: "text-neon-red border-neon-red/30 bg-neon-red/10",
};

interface Props {
  messages: DebateMessage[];
  userName?: string;
  userExpertise?: "beginner" | "intermediate" | "advanced";
}

export default function FinalVerdict({ messages, userName = "Trader", userExpertise = "beginner" }: Props) {
  // Derive votes from debate sentiment
  const agentVotes = agents.map((a) => {
    const agentMsgs = messages.filter((m) => m.agentId === a.id);
    const text = agentMsgs.map((m) => m.text).join(" ").toLowerCase();
    const bullish = (text.match(/buy|bullish|opportunity|momentum|ride|growth|strong|accumul/g) || []).length;
    const bearish = (text.match(/avoid|sell|risk|expensive|overvalued|falling|knife|stretched/g) || []).length;
    if (bullish > bearish + 1) return { ...a, vote: "BUY" as const };
    if (bearish > bullish + 1) return { ...a, vote: "AVOID" as const };
    return { ...a, vote: "HOLD" as const };
  });

  const votes = agentVotes.map((a) => a.vote);
  const buyCount = votes.filter((v) => v === "BUY").length;
  const holdCount = votes.filter((v) => v === "HOLD").length;
  const avoidCount = votes.filter((v) => v === "AVOID").length;
  const decision = buyCount >= 2 ? "BUY" : holdCount >= 2 ? "HOLD" : avoidCount >= 2 ? "AVOID" : "HOLD";

  if (messages.length === 0) {
    return (
      <div className="glass-card p-5 text-center text-sm text-muted-foreground">
        Final verdict will appear after the debate
      </div>
    );
  }

  // Build expertise-aware recommendation message
  const getRecommendationMessage = () => {
    if (decision === "BUY") {
      if (userExpertise === "beginner") {
        return `For ${userName}: This looks like a solid entry point. Start with a small position and monitor carefully.`;
      } else if (userExpertise === "intermediate") {
        return `For ${userName}: Strong fundamentals support an entry. Consider scaling in based on technical support levels.`;
      } else {
        return `For ${userName}: Compelling thesis with attractive risk-reward. Build position gradually near key support zones.`;
      }
    } else if (decision === "HOLD") {
      if (userExpertise === "beginner") {
        return `For ${userName}: This is neither a clear buy nor sell. Wait for better clarity or entry conditions.`;
      } else if (userExpertise === "intermediate") {
        return `For ${userName}: Fairly valued with mixed signals. Hold existing positions but avoid fresh entries for now.`;
      } else {
        return `For ${userName}: Mixed factors suggest maintaining current exposure. Watch for macro catalysts or technical breakouts.`;
      }
    } else {
      if (userExpertise === "beginner") {
        return `For ${userName}: This has too many risks. Better opportunities exist elsewhere. Stay away.`;
      } else if (userExpertise === "intermediate") {
        return `For ${userName}: Risk-reward unfavorable at current levels. Avoid entry; consider exit if holding.`;
      } else {
        return `For ${userName}: Risk factors outweigh fundamentals. Recommend risk-off position; wait for significant deterioration to reconsider.`;
      }
    }
  };

  return (
    <div className="glass-card p-6">
      {/* User recommendation header */}
      <div className="mb-6 pb-6 border-b border-secondary/30">
        <div className="text-center">
          <p className="text-xs uppercase tracking-widest text-muted-foreground mb-2">Verdict for {userName}</p>
          <div className={`inline-block text-3xl font-mono font-black px-8 py-3 rounded-xl border-2 ${voteStyle[decision]}`}>
            {decision}
          </div>
          <p className="text-sm text-muted-foreground mt-4 leading-relaxed">
            {getRecommendationMessage()}
          </p>
        </div>
      </div>

      {/* Agent votes breakdown */}
      <div className="flex items-center justify-between flex-wrap gap-4">
        <div>
          <h3 className="text-xs font-semibold uppercase tracking-widest text-muted-foreground mb-3">Agent Votes</h3>
          <div className="flex gap-3">
            {agentVotes.map((a) => (
              <div key={a.id} className="flex items-center gap-2">
                <AgentAvatar agent={a} size="sm" />
                <div>
                  <div className="text-[10px] text-muted-foreground">{a.name}</div>
                  <div className={`text-xs font-mono font-bold px-2 py-0.5 rounded border ${voteStyle[a.vote]}`}>
                    {a.vote}
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>

        <div className="flex gap-4 items-end">
          <VoteTally label="BUY" count={buyCount} total={3} color="bg-neon-green" />
          <VoteTally label="HOLD" count={holdCount} total={3} color="bg-neon-yellow" />
          <VoteTally label="AVOID" count={avoidCount} total={3} color="bg-neon-red" />
        </div>

        <div className="flex flex-col items-center gap-1">
          <span className="text-[10px] uppercase tracking-widest text-muted-foreground">Final Decision</span>
          <div className={`text-2xl font-mono font-black px-6 py-2 rounded-xl border-2 ${voteStyle[decision]}`}>
            {decision}
          </div>
        </div>
      </div>
    </div>
  );
}

function VoteTally({ label, count, total, color }: { label: string; count: number; total: number; color: string }) {
  return (
    <div className="flex flex-col items-center gap-1">
      <span className="text-[10px] text-muted-foreground font-mono">{label}</span>
      <div className="flex gap-1">
        {Array.from({ length: total }).map((_, i) => (
          <div key={i} className={`w-3 h-8 rounded-sm ${i < count ? color : "bg-secondary"} transition-colors`} />
        ))}
      </div>
      <span className="text-xs font-mono font-bold text-foreground">{count}/{total}</span>
    </div>
  );
}
