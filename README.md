# Agentic AI RFP Automation Platform

An Agentic AI system that automates RFP (Request for Proposal) analysis, technical matching, pricing estimation, and response orchestration using multiple collaborating AI agents.

This project was built for a hackathon and demonstrates real-world multi-agent AI workflows using sponsored tools.

---

## 🚀 Problem Statement

Organizations receive multiple RFPs regularly.  
Manually reviewing, prioritizing, matching products, and estimating pricing is time-consuming and error-prone.

---

## ✅ Solution Overview

We built an **Agentic AI workflow** where multiple AI agents collaborate autonomously:

- Identify urgent RFPs
- Understand technical scope
- Match OEM SKUs
- Estimate pricing
- Produce a consolidated response

---

## 🧠 Agentic AI Architecture

**Agents involved:**

### 1. Main Agent (Orchestrator)
- Starts and ends the workflow
- Coordinates all agents
- Consolidates final response

### 2. Sales Agent
- Scans multiple RFP files
- Extracts due dates
- Selects the most urgent RFP
- Summarizes business context

### 3. Technical Agent
- Extracts scope of supply
- Matches specs with OEM SKUs
- Calculates spec match percentage
- Recommends best products

### 4. Pricing Agent
- Uses dummy pricing tables
- Calculates material and testing cost
- Produces total cost per RFP item

---

## 🏗️ Tech Stack

- Frontend: Next.js
- Backend: FastAPI
- AI Model: Groq LLM
- Workflow Orchestration: Kestra
- Code Review: CodeRabbit
- Deployment: Vercel

---


---

## ⚙️ Setup Instructions

### Backend
```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
http://127.0.0.1:8000

Frontend
cd frontend
npm install
npm run dev


Frontend runs at:

http://localhost:3000

▶️ How to Use

Add RFP text files in:

data/rfps/


Open frontend in browser

Click Run Full RFP Workflow

View:

Sales summary

Technical SKU matches

Pricing table and total cost

🔄 Kestra Workflow

Kestra orchestrates the same agent flow using workflows:

Fetches backend results

Applies AI summarization and decisions

Provides execution logs

Flows are located in:

kestra/flows/

🏆 Sponsor Usage

Cline: Agent-based automation and development workflow

Kestra: AI workflow orchestration and decisioning

Oumi: LLM evaluation / judge agent (conceptual integration)

Vercel: Frontend deployment

CodeRabbit: PR reviews, documentation and code quality improvements

