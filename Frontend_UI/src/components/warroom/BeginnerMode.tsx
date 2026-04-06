import { Lightbulb } from "lucide-react";
import type { DebateMessage } from "./debateData";

interface Props {
  stockName: string;
  messages: DebateMessage[];
}

export default function BeginnerMode({ stockName, messages }: Props) {
  if (messages.length === 0) {
    return (
      <div className="glass-card p-5 text-center text-sm text-muted-foreground">
        <Lightbulb className="w-4 h-4 text-neon-yellow inline mr-2" />
        Beginner summary will appear after the debate
      </div>
    );
  }

  const points = [
    `Our AI analysts debated whether ${stockName} is a good investment right now — two of them think it has potential, while one prefers caution.`,
    `The aggressive trader sees growth momentum, the balanced analyst suggests buying in small amounts, and the safe investor wants to wait for a better price.`,
    `Overall: Don't put all your money in one stock. Start small, do your own research, and invest only what you can afford to lose.`,
  ];

  return (
    <div className="glass-card p-5">
      <div className="flex items-center gap-2 mb-3">
        <Lightbulb className="w-4 h-4 text-neon-yellow" />
        <h3 className="text-xs font-semibold uppercase tracking-widest text-neon-yellow">Explain Like I'm New to Investing</h3>
      </div>
      <ul className="space-y-2.5">
        {points.map((p, i) => (
          <li key={i} className="flex items-start gap-3 text-sm text-secondary-foreground leading-relaxed">
            <span className="mt-1 w-5 h-5 rounded-full bg-neon-yellow/10 text-neon-yellow text-[10px] font-bold flex items-center justify-center shrink-0">
              {i + 1}
            </span>
            {p}
          </li>
        ))}
      </ul>
    </div>
  );
}
