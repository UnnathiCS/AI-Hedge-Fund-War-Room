export interface Agent {
  id: "aggressive" | "balanced" | "safe";
  name: string;
  role: string;
  emoji: string;
  vote: "BUY" | "HOLD" | "AVOID";
}

export interface DebateMessage {
  agentId: Agent["id"];
  text: string;
  round: "Opening" | "Rebuttal" | "Final Verdict";
}

// Map backend agent names to frontend format
export function mapBackendAgent(agentName: string): Agent["id"] {
  const name = agentName.toLowerCase();
  if (name.includes("aggressive")) return "aggressive";
  if (name.includes("conservative") || name.includes("safe")) return "safe";
  return "balanced";
}

export const agents: Agent[] = [
  { id: "aggressive", name: "Aggressive", role: "Aggressive Trader", emoji: "🔥", vote: "BUY" },
  { id: "balanced", name: "Balanced", role: "Balanced Analyst", emoji: "📊", vote: "BUY" },
  { id: "safe", name: "Safe", role: "Conservative Investor", emoji: "🛡", vote: "HOLD" },
];

export const INDIAN_BROKERS = [
  "ICICI Securities",
  "YES Securities",
  "Axis Securities",
  "Reliance Securities",
  "HDFC Securities",
  "Kotak Securities",
  "SBI Securities",
  "IIFL Securities",
];

export const POPULAR_STOCKS = [
  { ticker: "ICICI Securities Limited", name: "ICICI Securities Limited" },
  { ticker: "Reliance Securities Limited", name: "Reliance Securities Limited" },
  { ticker: "HDFC Bank", name: "HDFC Bank" },
  { ticker: "ICICI Bank", name: "ICICI Bank" },
  { ticker: "HCL Technologies", name: "HCL Technologies" },
  { ticker: "Axis Bank", name: "Axis Bank" },
  { ticker: "Federal Bank", name: "Federal Bank" },
  { ticker: "Birla Corp", name: "Birla Corp" },
  { ticker: "State Bank", name: "State Bank" },
  { ticker: "Kotak Mahindra Bank", name: "Kotak Mahindra Bank" },
  { ticker: "IndusInd Bank", name: "IndusInd Bank" },
  { ticker: "Marico Ltd", name: "Marico Ltd" },
  { ticker: "Inox Wind Limited", name: "Inox Wind Limited" },
  { ticker: "Wipro Ltd", name: "Wipro Ltd" },
  { ticker: "Dixon Technologies", name: "Dixon Technologies" },
  { ticker: "Zensar Technologies", name: "Zensar Technologies" },
  { ticker: "ITC Ltd", name: "ITC Ltd" },
  { ticker: "Nuvoco Vistas Corp", name: "Nuvoco Vistas Corp" },
  { ticker: "Asian Paints Ltd", name: "Asian Paints Ltd" },
  { ticker: "Dabur India Ltd", name: "Dabur India Ltd" },
  { ticker: "Hindustan Unilever Ltd", name: "Hindustan Unilever Ltd" },
  { ticker: "Hero MotoCorp", name: "Hero MotoCorp" },
  { ticker: "RBL Bank", name: "RBL Bank" },
  { ticker: "City Union Bank", name: "City Union Bank" },
  { ticker: "Indian Oil Corp", name: "Indian Oil Corp" },
];

/**
 * Convert backend debate messages to frontend format
 * Backend sends: { agent: "Aggressive", round: "Opening", text: "..." }
 * Frontend expects: { agentId: "aggressive", round: "Opening", text: "..." }
 */
export function convertBackendMessages(
  backendMessages: Array<{ agent: string; round: string; text: string }>
): DebateMessage[] {
  return backendMessages.map((msg) => ({
    agentId: mapBackendAgent(msg.agent),
    text: msg.text,
    round: (msg.round as "Opening" | "Rebuttal" | "Final Verdict") || "Opening",
  }));
}
