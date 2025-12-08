# Agents
Sales Agent

Inputs: list of RFP URLs

Outputs: chosen RFP JSON (id, title, due date, scope, doc link)

Technical Agent

Inputs: RFP summary + RFP doc, OEM product data

Outputs: spec match table (top 3 SKUs per product + spec match %)

Pricing Agent

Inputs: chosen SKUs, quantities, test requirements, pricing tables

Outputs: per-item + total pricing

Main Agent

Orchestrates the above, returns final structured response.