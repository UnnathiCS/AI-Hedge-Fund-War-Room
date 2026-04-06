const corsHeaders = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Headers": "authorization, x-client-info, apikey, content-type",
};

const YAHOO_FINANCE_URL = "https://query1.finance.yahoo.com/v8/finance/chart";

Deno.serve(async (req) => {
  if (req.method === "OPTIONS") {
    return new Response("ok", { headers: corsHeaders });
  }

  try {
    const { ticker } = await req.json();
    if (!ticker || typeof ticker !== "string") {
      return new Response(JSON.stringify({ error: "ticker is required" }), {
        status: 400,
        headers: { ...corsHeaders, "Content-Type": "application/json" },
      });
    }

    const symbol = ticker.toUpperCase().trim();

    // Fetch from Yahoo Finance
    const url = `${YAHOO_FINANCE_URL}/${encodeURIComponent(symbol)}?range=1y&interval=1d&includePrePost=false`;
    const response = await fetch(url, {
      headers: {
        "User-Agent": "Mozilla/5.0",
      },
    });

    if (!response.ok) {
      return new Response(
        JSON.stringify({ error: `Stock not found: ${symbol}` }),
        {
          status: 404,
          headers: { ...corsHeaders, "Content-Type": "application/json" },
        }
      );
    }

    const data = await response.json();
    const result = data?.chart?.result?.[0];
    if (!result) {
      return new Response(
        JSON.stringify({ error: `No data for ${symbol}` }),
        {
          status: 404,
          headers: { ...corsHeaders, "Content-Type": "application/json" },
        }
      );
    }

    const meta = result.meta;
    const closes = result.indicators?.quote?.[0]?.close || [];
    const currentPrice = meta.regularMarketPrice || 0;
    const previousClose = meta.chartPreviousClose || meta.previousClose || currentPrice;
    const change = currentPrice - previousClose;
    const changePercent = previousClose ? (change / previousClose) * 100 : 0;

    // Calculate 1Y return
    const firstClose = closes.find((c: number | null) => c !== null) || currentPrice;
    const oneYearReturn = firstClose ? ((currentPrice - firstClose) / firstClose) * 100 : 0;

    // Estimate volatility from daily returns
    const validCloses = closes.filter((c: number | null) => c !== null);
    let volatility = "Medium";
    if (validCloses.length > 20) {
      const returns: number[] = [];
      for (let i = 1; i < validCloses.length; i++) {
        if (validCloses[i - 1] > 0) {
          returns.push((validCloses[i] - validCloses[i - 1]) / validCloses[i - 1]);
        }
      }
      const mean = returns.reduce((a, b) => a + b, 0) / returns.length;
      const variance = returns.reduce((a, b) => a + (b - mean) ** 2, 0) / returns.length;
      const annualizedVol = Math.sqrt(variance * 252) * 100;
      volatility = annualizedVol > 40 ? "High" : annualizedVol > 20 ? "Medium" : "Low";
    }

    const risk = volatility === "High" ? "high" : volatility === "Low" ? "low" : "medium";

    const stockData = {
      name: meta.longName || meta.shortName || symbol,
      ticker: symbol,
      price: currentPrice,
      change: Math.round(change * 100) / 100,
      changePercent: Math.round(changePercent * 100) / 100,
      pe: 0, // Yahoo chart API doesn't provide P/E
      volatility,
      oneYearReturn: Math.round(oneYearReturn * 10) / 10,
      risk,
      currency: meta.currency || "USD",
    };

    return new Response(JSON.stringify(stockData), {
      headers: { ...corsHeaders, "Content-Type": "application/json" },
    });
  } catch (error) {
    console.error("Error fetching stock data:", error);
    return new Response(
      JSON.stringify({ error: "Failed to fetch stock data" }),
      {
        status: 500,
        headers: { ...corsHeaders, "Content-Type": "application/json" },
      }
    );
  }
});
