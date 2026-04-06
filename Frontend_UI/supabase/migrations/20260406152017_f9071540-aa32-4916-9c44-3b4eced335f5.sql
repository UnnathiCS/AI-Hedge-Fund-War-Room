
CREATE TABLE public.debate_sessions (
  id UUID NOT NULL DEFAULT gen_random_uuid() PRIMARY KEY,
  broker TEXT NOT NULL,
  ticker TEXT NOT NULL,
  company_name TEXT NOT NULL,
  stock_price NUMERIC,
  pe_ratio NUMERIC,
  change_percent NUMERIC,
  verdict TEXT NOT NULL CHECK (verdict IN ('BUY', 'HOLD', 'AVOID')),
  debate_messages JSONB NOT NULL DEFAULT '[]',
  analytics JSONB NOT NULL DEFAULT '{}',
  created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now()
);

ALTER TABLE public.debate_sessions ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Anyone can view debate sessions"
ON public.debate_sessions FOR SELECT USING (true);

CREATE POLICY "Anyone can create debate sessions"
ON public.debate_sessions FOR INSERT WITH CHECK (true);
