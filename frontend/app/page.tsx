"use client";

import { useState } from "react";

export default function Home() {
  const [loading, setLoading] = useState(false);
  const [data, setData] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);

  const runFullFlow = async () => {
    try {
      setLoading(true);
      setError(null);

      const res = await fetch("http://127.0.0.1:8000/rfp/full-run");
      const json = await res.json();

      if (!res.ok) {
        throw new Error(json?.detail || "Request failed");
      }

      console.log("FULL BACKEND RESPONSE:", json); // DEBUG (can remove later)
      setData(json);
    } catch (e: any) {
      setError(e.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="min-h-screen p-8 space-y-8 bg-white text-gray-900">

      {/* HEADER */}
      <header className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-black">
            Asian Paints – RFP Agentic AI (Demo)
          </h1>
          <p className="text-base text-gray-800 mt-1">
            Sales • Technical • Pricing • Orchestrator
          </p>
        </div>

        <button
          onClick={runFullFlow}
          disabled={loading}
          className="px-4 py-2 rounded-md bg-blue-700 text-white text-sm font-semibold hover:bg-blue-800 disabled:opacity-60"
        >
          {loading ? "Running workflow..." : "Run Full RFP Workflow"}
        </button>
      </header>

      {/* ERROR */}
      {error && (
        <div className="p-3 rounded-md bg-red-200 text-red-900 text-sm font-semibold">
          Error: {error}
        </div>
      )}

      {!data && !loading && !error && (
        <p className="text-gray-900 text-lg font-medium">
          Click <strong>“Run Full RFP Workflow”</strong> to begin.
        </p>
      )}

      {data && (
        <section className="space-y-6">

          {/* SALES SUMMARY */}
          <section className="p-4 bg-gray-100 rounded-lg shadow border border-gray-300">
            <h2 className="text-xl font-bold text-black">Sales Summary</h2>

            <div className="mt-3 space-y-1">
              <p><strong>RFP ID:</strong> {data?.sales_summary?.rfp_id}</p>
              <p><strong>Title:</strong> {data?.sales_summary?.title}</p>
              <p><strong>Due Date:</strong> {data?.sales_summary?.due_date}</p>
              <p className="mt-2">
                <strong>Scope Summary:</strong><br />
                {data?.sales_summary?.scope_summary}
              </p>
            </div>
          </section>

          {/* TECHNICAL */}
          <section className="p-4 bg-gray-100 rounded-lg shadow border border-gray-300">
            <h2 className="text-xl font-bold text-black">Technical – Spec Match</h2>

            {(data?.technical?.items ?? []).length === 0 ? (
              <p className="text-sm mt-2">No technical items found.</p>
            ) : (
              <div className="space-y-4 mt-3">
                {data.technical.items.map((item: any, idx: number) => (
                  <div key={idx} className="border p-3 bg-white rounded">
                    <p className="font-bold mb-2">
                      RFP Item: <span className="font-normal">{item.rfp_item}</span>
                    </p>

                    {item.top_matches.length === 0 ? (
                      <p>No SKU matches found.</p>
                    ) : (
                      <table className="w-full text-sm border">
                        <thead className="bg-gray-300">
                          <tr>
                            <th className="border px-2 py-1">SKU</th>
                            <th className="border px-2 py-1">Score</th>
                            <th className="border px-2 py-1">Cores</th>
                            <th className="border px-2 py-1">Area</th>
                            <th className="border px-2 py-1">Insulation</th>
                            <th className="border px-2 py-1">Material</th>
                            <th className="border px-2 py-1">Voltage</th>
                          </tr>
                        </thead>
                        <tbody>
                          {item.top_matches.map((m: any, j: number) => (
                            <tr key={j}>
                              <td className="border px-2 py-1">{m.sku_id}</td>
                              <td className="border px-2 py-1">{m.score}</td>
                              <td className="border px-2 py-1">{m.cores}</td>
                              <td className="border px-2 py-1">{m.area_sqmm}</td>
                              <td className="border px-2 py-1">{m.insulation}</td>
                              <td className="border px-2 py-1">{m.material}</td>
                              <td className="border px-2 py-1">{m.voltage}</td>
                            </tr>
                          ))}
                        </tbody>
                      </table>
                    )}
                  </div>
                ))}
              </div>
            )}
          </section>

          {/* PRICING */}
          <section className="p-4 bg-gray-100 rounded-lg shadow border border-gray-300">
            <h2 className="text-xl font-bold text-black">Pricing</h2>

            <table className="w-full text-sm border mt-3">
              <thead className="bg-gray-300">
                <tr>
                  <th className="border px-2 py-1">RFP Item</th>
                  <th className="border px-2 py-1">Best SKU</th>
                  <th className="border px-2 py-1">Match %</th>
                  <th className="border px-2 py-1">Total Cost</th>
                </tr>
              </thead>
              <tbody>
                {(data?.pricing?.priced_items ?? []).map((p: any, idx: number) => (
                  <tr key={idx}>
                    <td className="border px-2 py-1">{p.rfp_item}</td>
                    <td className="border px-2 py-1">{p.best_match_sku ?? "-"}</td>
                    <td className="border px-2 py-1">{p.match_score ?? "-"}</td>
                    <td className="border px-2 py-1">
                      {p.pricing?.total_cost
                        ? `₹${p.pricing.total_cost}`
                        : "-"}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>

            {/* GRAND TOTAL */}
            {data.pricing?.grand_total !== undefined && (
              <div className="text-right mt-4 text-lg font-bold text-black">
                Grand Total: ₹{data.pricing.grand_total}
            </div>
            )}
            
          </section>
          
          <section>
            <h2>Oumi Judge Evaluation</h2>
            {data.oumi_judgement.judged_items.map((j:any, i:number) => (
              <p key={i}>
                {j.rfp_item} → Score: {j.judge_score}
              </p>
            ))}
          </section>      
          
        </section>
      )}
    </main>
  );
}
