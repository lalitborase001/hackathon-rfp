from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from agents.sales_agent import SalesAgent
from agents.technical_agent import TechnicalAgent
from agents.pricing_agent import PricingAgent
from agents.oumi_judge_agent import OumiJudgeAgent



app = FastAPI(title="Asian Paints RFP Agentic Backend")

origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.get("/sales/run")
def sales_run():
    """
    Run the Sales Agent on the first available RFP file.
    """
    try:
        sales_agent = SalesAgent()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to initialize SalesAgent: {e}")

    rfps = sales_agent.list_available_rfps()
    if not rfps:
        raise HTTPException(status_code=404, detail="No RFP files found in data/rfps")

    rfp_file = rfps[0]

    try:
        info = sales_agent.summarize_rfp(rfp_file)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error summarizing RFP: {e}")

    return {
        "rfp_id": info.rfp_id,
        "title": info.title,
        "due_date": info.due_date,
        "scope_summary": info.scope_summary,
        "file_path": info.file_path,
    }

@app.get("/technical/run")
def technical_run():
    """
    Run the Technical Agent on the first available RFP file.
    """
    try:
        sales_agent = SalesAgent()
        technical_agent = TechnicalAgent()
    except Exception as e:
        # This catches issues like missing sku.csv etc. during init
        raise HTTPException(status_code=500, detail=f"Failed to initialize agents: {e}")

    # Find RFP file
    rfps = sales_agent.list_available_rfps()
    if not rfps:
        raise HTTPException(status_code=404, detail="No RFP files found in data/rfps")

    rfp_file = rfps[0]

    # Read RFP text
    try:
        with open(rfp_file, "r", encoding="utf-8") as f:
            rfp_text = f.read()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading RFP file: {e}")

    # Run TechnicalAgent
    try:
        result = technical_agent.match_specs(rfp_text)
    except Exception as e:
        # Also print stack trace to console for you
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Error in TechnicalAgent.match_specs: {e}")

    # Return JSON-serializable result
    return result

@app.get("/pricing/run")
def pricing_run():
    """
    Run Technical Agent + Pricing Agent in sequence on the first RFP.
    """
    # 1) Init agents
    try:
        sales_agent = SalesAgent()
        technical_agent = TechnicalAgent()
        pricing_agent = PricingAgent()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to initialize agents: {e}")

    # 2) Find RFP file
    rfps = sales_agent.list_available_rfps()
    if not rfps:
        raise HTTPException(status_code=404, detail="No RFP files found in data/rfps")
    rfp_file = rfps[0]

    # 3) Read RFP text
    try:
        with open(rfp_file, "r", encoding="utf-8") as f:
            rfp_text = f.read()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading RFP file: {e}")

    # 4) Technical matching
    try:
        technical_result = technical_agent.match_specs(rfp_text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error in TechnicalAgent: {e}")

    # 5) Pricing based on technical result
    try:
        pricing_result = pricing_agent.price_from_technical_result(technical_result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error in PricingAgent: {e}")

    # 6) Return combined result
    return {
        "rfp_file": rfp_file,
        "technical": technical_result,
        "pricing": pricing_result,
    }
@app.get("/rfp/full-run")
def full_rfp_run():
    """
    Orchestrator endpoint:
    Runs Sales, Technical, Oumi Judge, and Pricing agents.
    """
    # 1) Init agents
    try:
        sales_agent = SalesAgent()
        technical_agent = TechnicalAgent()
        pricing_agent = PricingAgent()
        oumi_judge_agent = OumiJudgeAgent()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to initialize agents: {e}")

    # 2) Find RFP file (earliest due handled inside SalesAgent if implemented)
    rfps = sales_agent.list_available_rfps()
    if not rfps:
        raise HTTPException(status_code=404, detail="No RFP files found in data/rfps")

    rfp_file = rfps[0]

    # 3) Read RFP text
    try:
        with open(rfp_file, "r", encoding="utf-8") as f:
            rfp_text = f.read()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading RFP file: {e}")

    # 4) Sales Agent (summary)
    try:
        sales_info = sales_agent.summarize_rfp(rfp_file)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error in SalesAgent: {e}")

    # 5) Technical Agent (spec matching)
    try:
        technical_result = technical_agent.match_specs(rfp_text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error in TechnicalAgent: {e}")

    # 6) 🧠 OUMI JUDGE AGENT (Evaluation / Reward Signal)
    try:
        oumi_judgement = oumi_judge_agent.evaluate_technical_output(technical_result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error in OumiJudgeAgent: {e}")

    # 7) Pricing Agent
    try:
        pricing_result = pricing_agent.price_from_technical_result(technical_result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error in PricingAgent: {e}")

    # 8) Final orchestrated response
    return {
        "rfp_file": rfp_file,
        "sales_summary": {
            "rfp_id": sales_info.rfp_id,
            "title": sales_info.title,
            "due_date": sales_info.due_date,
            "scope_summary": sales_info.scope_summary,
        },
        "technical": technical_result,
        "oumi_judgement": oumi_judgement,
        "pricing": pricing_result,
    }


