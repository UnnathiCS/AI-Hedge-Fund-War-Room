import type { Agent } from "./debateData";

const dotColor = {
  aggressive: "bg-agent-aggressive",
  balanced: "bg-agent-balanced",
  safe: "bg-agent-conservative",
};

export default function TypingIndicator({ agentId }: { agentId: Agent["id"] }) {
  return (
    <div className="flex items-center gap-1 px-3 py-2">
      <div className={`w-1.5 h-1.5 rounded-full ${dotColor[agentId]} animate-typing-dot-1`} />
      <div className={`w-1.5 h-1.5 rounded-full ${dotColor[agentId]} animate-typing-dot-2`} />
      <div className={`w-1.5 h-1.5 rounded-full ${dotColor[agentId]} animate-typing-dot-3`} />
    </div>
  );
}
