import { useState, useEffect, useRef } from "react";
import { agents, type DebateMessage, type Agent } from "./debateData";
import AgentAvatar from "./AgentAvatar";
import TypingIndicator from "./TypingIndicator";

const bubbleBg = {
  aggressive: "bg-agent-aggressive/10 border-agent-aggressive/20",
  balanced: "bg-agent-balanced/10 border-agent-balanced/20",
  safe: "bg-agent-conservative/10 border-agent-conservative/20",
};

const nameColor = {
  aggressive: "text-agent-aggressive",
  balanced: "text-agent-balanced",
  safe: "text-agent-conservative",
};

interface DebateRoomProps {
  messages: DebateMessage[];
  isActive: boolean;
}

export default function DebateRoom({ messages, isActive }: DebateRoomProps) {
  const [visibleMessages, setVisibleMessages] = useState<DebateMessage[]>([]);
  const [typingAgent, setTypingAgent] = useState<Agent["id"] | null>(null);
  const scrollRef = useRef<HTMLDivElement>(null);
  const indexRef = useRef(0);

  // Display messages with typing animation
  useEffect(() => {
    if (!isActive || messages.length === 0) return;
    setVisibleMessages([]);
    setTypingAgent(null);
    indexRef.current = 0;

    const showNext = () => {
      const idx = indexRef.current;
      if (idx >= messages.length) {
        setTypingAgent(null);
        return;
      }

      const msg = messages[idx];
      setTypingAgent(msg.agentId);

      const typingDelay = 1200 + Math.random() * 800;
      const timer = setTimeout(() => {
        setTypingAgent(null);
        setVisibleMessages((prev) => [...prev, msg]);
        indexRef.current++;

        const nextDelay = 600 + Math.random() * 400;
        setTimeout(showNext, nextDelay);
      }, typingDelay);

      return () => clearTimeout(timer);
    };

    const startDelay = setTimeout(showNext, 800);
    return () => {
      clearTimeout(startDelay);
    };
  }, [messages, isActive]);

  useEffect(() => {
    scrollRef.current?.scrollTo({ top: scrollRef.current.scrollHeight, behavior: "smooth" });
  }, [visibleMessages, typingAgent]);

  const currentSpeaker = typingAgent || visibleMessages[visibleMessages.length - 1]?.agentId;

  return (
    <div className="glass-card flex flex-col h-full">
      {/* Header */}
      <div className="flex items-center justify-between px-5 py-3 border-b border-border">
        <div className="flex items-center gap-3">
          <div className={`w-2 h-2 rounded-full ${isActive ? "bg-neon-red animate-pulse" : "bg-muted-foreground"}`} />
          <h2 className="text-sm font-semibold uppercase tracking-widest text-foreground">
            {isActive ? "Live Debate Room" : "Debate Room"}
          </h2>
        </div>
        <div className="flex -space-x-2">
          {agents.map((a) => (
            <AgentAvatar key={a.id} agent={a} isSpeaking={isActive && currentSpeaker === a.id} size="sm" />
          ))}
        </div>
      </div>

      {/* Messages */}
      <div ref={scrollRef} className="flex-1 overflow-y-auto px-5 py-4 space-y-4 min-h-0">
        {!isActive && visibleMessages.length === 0 && (
          <div className="flex items-center justify-center h-full text-muted-foreground text-sm">
            Select a stock and click <span className="text-neon-green font-semibold mx-1">Start Debate</span> to begin
          </div>
        )}

        {visibleMessages.map((msg, i) => {
          const agent = agents.find((a) => a.id === msg.agentId)!;
          return (
            <div key={i} className="flex items-start gap-3 animate-slide-up">
              <AgentAvatar agent={agent} isSpeaking={currentSpeaker === agent.id} />
              <div className="flex-1 min-w-0">
                <div className="flex items-center gap-2 mb-1">
                  <span className={`text-xs font-semibold ${nameColor[agent.id]}`}>{agent.emoji} {agent.name}</span>
                  <span className="text-[10px] text-muted-foreground">{agent.role}</span>
                </div>
                <div className={`inline-block px-4 py-2.5 rounded-2xl rounded-tl-sm border text-sm leading-relaxed text-foreground ${bubbleBg[agent.id]}`}>
                  {msg.text}
                </div>
              </div>
            </div>
          );
        })}

        {typingAgent && (
          <div className="flex items-start gap-3">
            <AgentAvatar agent={agents.find((a) => a.id === typingAgent)!} isSpeaking />
            <div className="flex-1">
              <div className="flex items-center gap-2 mb-1">
                <span className={`text-xs font-semibold ${nameColor[typingAgent]}`}>
                  {agents.find((a) => a.id === typingAgent)!.emoji} {agents.find((a) => a.id === typingAgent)!.name}
                </span>
              </div>
              <div className={`inline-block px-4 py-2 rounded-2xl rounded-tl-sm border ${bubbleBg[typingAgent]}`}>
                <TypingIndicator agentId={typingAgent} />
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
