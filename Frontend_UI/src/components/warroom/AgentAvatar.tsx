import { cn } from "@/lib/utils";
import type { Agent } from "./debateData";

const colorMap = {
  aggressive: "border-agent-aggressive neon-glow-red",
  balanced: "border-agent-balanced neon-glow-blue",
  safe: "border-agent-conservative neon-glow-green",
};

const bgMap = {
  aggressive: "bg-agent-aggressive/20",
  balanced: "bg-agent-balanced/20",
  safe: "bg-agent-conservative/20",
};

interface Props {
  agent: Agent;
  isSpeaking?: boolean;
  size?: "sm" | "md";
}

export default function AgentAvatar({ agent, isSpeaking = false, size = "md" }: Props) {
  const dim = size === "md" ? "w-12 h-12 text-xl" : "w-8 h-8 text-sm";

  return (
    <div
      className={cn(
        "rounded-full border-2 flex items-center justify-center transition-all duration-500",
        dim,
        bgMap[agent.id],
        isSpeaking ? colorMap[agent.id] : "border-border"
      )}
    >
      <span className={isSpeaking ? "animate-pulse-glow" : ""}>{agent.emoji}</span>
    </div>
  );
}
