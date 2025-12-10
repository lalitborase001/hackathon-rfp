import os
import json
from dataclasses import dataclass
from typing import List
from pathlib import Path

from dotenv import load_dotenv
from groq import Groq

# Load .env from project root
load_dotenv()


@dataclass
class RFPInfo:
    rfp_id: str
    title: str
    due_date: str
    scope_summary: str
    file_path: str


class SalesAgent:
    def __init__(self) -> None:
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise RuntimeError("GROQ_API_KEY is missing in .env")
        self.client = Groq(api_key=api_key)

    def _project_root(self) -> Path:
        # backend/agents/sales_agent.py → backend/agents → backend → project root
        backend_dir = Path(__file__).resolve().parent.parent  # /backend
        return backend_dir.parent  # /hackathon-rfp

    def list_available_rfps(self) -> List[str]:
        """
        Return a list of full paths to .txt RFP files under project-root/data/rfps.
        """
        rfp_dir = self._project_root() / "data" / "rfps"
        if not rfp_dir.is_dir():
            return []

        return [
            str(p)
            for p in rfp_dir.glob("*.txt")
        ]

    def _read_rfp_text(self, file_path: str) -> str:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()

    def summarize_rfp(self, file_path: str) -> RFPInfo:
        """
        Read an RFP file and ask Groq LLM to return structured JSON.
        """
        text = self._read_rfp_text(file_path)

        prompt = f"""
You are an assistant that extracts key information from RFP documents.

Given the following RFP text, extract:
- RFP ID (or create one if missing)
- Title
- Bid submission due date (as written)
- A short 3–4 line scope summary

Return the result as STRICT JSON with the following keys:
rfp_id, title, due_date, scope_summary

RFP TEXT:
{text}
        """.strip()

        # Call Groq chat completions API
        response = self.client.chat.completions.create(
            # if this model name errors, check Groq docs and adjust it
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "You extract structured data from RFPs and always respond in JSON."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.1,
        )

        content = response.choices[0].message.content

        # Try to parse JSON
        try:
            data = json.loads(content)
        except json.JSONDecodeError:
            # Fallback: try to extract JSON object substring
            import re

            match = re.search(r"\{.*\}", content, re.DOTALL)
            if not match:
                raise RuntimeError(f"Could not parse JSON from LLM response: {content}")
            data = json.loads(match.group(0))

        return RFPInfo(
            rfp_id=data.get("rfp_id", "UNKNOWN"),
            title=data.get("title", "UNKNOWN"),
            due_date=data.get("due_date", "UNKNOWN"),
            scope_summary=data.get("scope_summary", ""),
            file_path=file_path,
        )
