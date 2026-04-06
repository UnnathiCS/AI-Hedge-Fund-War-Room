/**
 * Backend API Integration Service
 * Connects to the Python FastAPI debate_engine backend
 */

export interface UserInfo {
  name: string;
  gender: "male" | "female" | "other";
  expertise: "beginner" | "intermediate" | "advanced";
}

export interface BackendMarketData {
  current_price: number;
  pe_ratio: number;
  volatility: number;
  one_year_return: number;
}

export interface BackendDebateMessage {
  agent: string;
  round: string;
  text: string;
}

export interface BackendDebateResponse {
  market_data: BackendMarketData;
  debate_messages: BackendDebateMessage[];
}

const BACKEND_BASE_URL = "http://localhost:8501";

/**
 * Fetch market data and run debate from backend
 */
export async function runDebate(
  company: string,
  ticker: string,
  userInfo?: UserInfo
): Promise<BackendDebateResponse> {
  try {
    const response = await fetch(`${BACKEND_BASE_URL}/api/debate`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ 
        company, 
        ticker,
        user_name: userInfo?.name || "",
        user_gender: userInfo?.gender || "other",
        user_expertise: userInfo?.expertise || "beginner"
      }),
    });

    if (!response.ok) {
      throw new Error(`Backend error: ${response.status} ${response.statusText}`);
    }

    const data: BackendDebateResponse = await response.json();
    return data;
  } catch (error) {
    console.error("Failed to run debate:", error);
    throw error;
  }
}

/**
 * Fetch only market data
 */
export async function fetchMarketData(ticker: string): Promise<BackendMarketData> {
  try {
    const response = await fetch(`${BACKEND_BASE_URL}/api/market-data/${ticker}`);

    if (!response.ok) {
      throw new Error(`Failed to fetch market data: ${response.status}`);
    }

    const data: BackendMarketData = await response.json();
    return data;
  } catch (error) {
    console.error("Failed to fetch market data:", error);
    throw error;
  }
}

/**
 * Fetch stock price with full details (price, change, PE, etc)
 */
export async function fetchStockDetails(ticker: string) {
  try {
    const response = await fetch(`${BACKEND_BASE_URL}/api/stock/${ticker}`);

    if (!response.ok) {
      throw new Error(`Failed to fetch stock details: ${response.status}`);
    }

    const data = await response.json();
    return data;
  } catch (error) {
    console.error("Failed to fetch stock details:", error);
    throw error;
  }
}
