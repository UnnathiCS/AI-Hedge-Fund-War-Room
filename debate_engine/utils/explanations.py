def reliability_explanation():
    return """
### Reliability Score

Formula:
Reliability = (1 / Rating Volatility) × (1 / Stance Changes)

Why?

If a broker changes ratings too often → unreliable.
If ratings fluctuate wildly → unstable.

So we reward:
- Stability
- Consistency
- Conviction

In simple terms:
A reliable broker is one who doesn’t panic or flip opinions frequently.
"""