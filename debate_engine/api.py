"""
FastAPI Backend Server for AI Hedge Fund War Room
Connects React Frontend to Python Debate Engine
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict
import pandas as pd
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import debate engines
from engines.market_data_engine import fetch_market_data
from engines.debate_engine import multi_round_debate
from engines.company_engine import compute_company_scores
from engines.broker_engine import compute_broker_profiles
from engines.weighting_engine import compute_weighted_ratings

app = FastAPI(title="AI Hedge Fund War Room API")

# Enable CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000", "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load dataset and compute ratings
try:
    df = pd.read_csv("debate_engine/dataset/final_dataset_cleaned.csv")
    
    # Extract company data directly without using weighting engine
    company_data = df[df['company'] != 'UNKNOWN'].groupby('company').agg({
        'broker': 'count',
        'rating': lambda x: (x == 'BUY').sum() / len(x) if len(x) > 0 else 0.5
    }).reset_index()
    company_data.columns = ['company', 'broker_count', 'weighted_rating']
    
    # Create lookup dictionary
    company_lookup = {}
    for idx, row in company_data.iterrows():
        company = row.get("company", "")
        if company:
            company_lookup[company] = {
                "weighted_rating": float(row.get("weighted_rating", 0.75)),
                "consensus_strength": float(row.get("weighted_rating", 0.75)) * 0.9,
                "disagreement": 0.35 * (1 - float(row.get("weighted_rating", 0.75))),
                "broker_count": int(row.get("broker_count", 1))
            }
    
    print(f"✅ Loaded {len(company_lookup)} companies from dataset")
except Exception as e:
    print(f"⚠️  Warning: Could not load dataset: {e}")
    company_lookup = {}
    df = pd.DataFrame()

# ============================================================================
# REQUEST/RESPONSE MODELS
# ============================================================================

class DebateRequest(BaseModel):
    company: str
    ticker: str = None
    user_name: str = ""
    user_gender: str = "other"  # male, female, or other
    user_expertise: str = "beginner"  # beginner, intermediate, or advanced

class DebateMessage(BaseModel):
    agent: str
    round: str
    text: str

class MarketData(BaseModel):
    current_price: float
    pe_ratio: float
    volatility: float
    one_year_return: float

class DebateResponse(BaseModel):
    market_data: MarketData
    debate_messages: List[DebateMessage]

# ============================================================================
# HEALTH CHECK
# ============================================================================

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "ok",
        "service": "AI Hedge Fund War Room API",
        "dataset_loaded": len(company_lookup) > 0
    }

# ============================================================================
# DEBATE ENDPOINT
# ============================================================================

@app.post("/api/debate", response_model=DebateResponse)
async def run_debate(request: DebateRequest):
    """
    Run multi-agent debate on a company
    
    Args:
        company: Company name (e.g., "HDFC Bank")
        ticker: Stock ticker (optional, for market data)
        user_name: User's name for personalization
        user_gender: User's gender ("male", "female", or "other")
    
    Returns:
        DebateResponse with market data and debate messages
    """
    try:
        company = request.company.strip()
        ticker = request.ticker or company  # Use ticker if provided, else company name
        user_name = request.user_name.strip()
        user_gender = request.user_gender.lower()
        user_expertise = request.user_expertise.lower()
        
        # Validate company exists in dataset
        if company not in company_lookup:
            # Try to find similar company
            similar = [c for c in company_lookup.keys() if company.lower() in c.lower()]
            if similar:
                company = similar[0]
            else:
                # Return error with available companies
                available = list(company_lookup.keys())[:10]
                raise HTTPException(
                    status_code=400,
                    detail=f"Company '{request.company}' not found. Try one of: {available}"
                )
        
        # Fetch market data
        try:
            market_data = fetch_market_data(ticker)
        except Exception as e:
            # Use synthetic data if yfinance fails
            market_data = {
                "current_price": 2500.0 + (hash(ticker) % 1000),
                "pe_ratio": 25.0 + (hash(ticker) % 10),
                "volatility": 0.25,
                "one_year_return": 0.15 + (hash(ticker) % 20) / 100
            }
        
        # Get institutional data from dataset
        company_data = company_lookup.get(company, {})
        institutional_data = {
            "weighted_rating": company_data.get("weighted_rating", 0.75),
            "consensus_strength": company_data.get("consensus_strength", 0.70),
            "disagreement": company_data.get("disagreement", 0.35)
        }
        
        # Prepare user context for debate engine
        user_context = {
            "name": user_name,
            "gender": user_gender,
            "expertise": user_expertise
        }
        
        # Run debate engine with user context
        debate_messages = multi_round_debate(company, market_data, institutional_data, user_context)
        
        # Format response
        formatted_messages = []
        for msg in debate_messages:
            formatted_messages.append({
                "agent": msg.get("agent", "Unknown"),
                "round": msg.get("round", "Opening"),
                "text": msg.get("text", "")
            })
        
        return DebateResponse(
            market_data=MarketData(**market_data),
            debate_messages=formatted_messages
        )
    
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Debate error: {str(e)}")

# ============================================================================
# AVAILABLE COMPANIES ENDPOINT
# ============================================================================

@app.get("/api/companies")
async def get_available_companies():
    """Get list of available companies for debate"""
    companies = sorted(list(company_lookup.keys()))
    return {
        "total": len(companies),
        "companies": companies
    }

# ============================================================================
# BROKER PROFILES ENDPOINT
# ============================================================================

@app.get("/api/brokers")
async def get_brokers():
    """Get list of brokers in dataset"""
    try:
        brokers = df['broker_clean'].unique().tolist() if not df.empty else []
        return {
            "total": len(brokers),
            "brokers": brokers
        }
    except:
        return {
            "total": 0,
            "brokers": []
        }

# ============================================================================
# RUN SERVER
# ============================================================================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8501,
        log_level="error"
    )
