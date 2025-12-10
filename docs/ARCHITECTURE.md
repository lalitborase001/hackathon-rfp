# Architecture
Overall system diagram (even in text for now):

Vercel (frontend) → Backend API → Kestra flows → Together.ai

Mention your tools:

Cline for dev, CodeRabbit for reviews, Oumi for future model tuning.

Data flow:

Sales Agent finds an RFP.

Technical Agent maps RFP specs ↔ OEM SKUs.

Pricing Agent computes costs.

Main Agent aggregates and returns final response.