# Kestra local demo

1. Start Kestra (from repo root):
   docker compose -f kestra/docker-compose.yml up -d

2. Open Kestra UI:
   http://localhost:8080

3. Add your AI provider API key as a secret in Kestra:
   - Key name: OPENAI_API_KEY (or whichever provider you configured)
   - In Docker demo you can set secrets in the UI or mount config.

4. Upload the flow YAML:
   - In Kestra UI -> Flows -> Create -> Paste YAML from kestra/flows/rfp_summarize_and_decide.yml

5. Run the flow (click Execute). Ensure backend is running at http://host.docker.internal:8000

6. Inspect the agent output (summary + decision) in the execution logs.
