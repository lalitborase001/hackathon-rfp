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
      if (!res.ok) throw new Error(json.detail || "Request failed");
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

      {/* INITIAL MESSAGE */}
      {!data && !error && !loading && (
        <p className="text-gray-900 text-lg font-medium">
          Click <span className="font-bold">“Run Full RFP Workflow”</span> to begin.
        </p>
      )}

      {data && (
        <section className="space-y-6">

          {/* SALES SUMMARY */}
          <section className="p-4 bg-gray-100 rounded-lg shadow border border-gray-300">
            <h2 className="text-xl font-bold text-black">Sales Summary</h2>
            <p className="text-sm text-gray-900 mt-2">
              <strong>RFP File:</strong> {data.rfp_file}
            </p>

            <div className="mt-4 space-y-1 text-gray-900">
              <p><strong>RFP ID:</strong> {data.sales_summary.rfp_id}</p>
              <p><strong>Title:</strong> {data.sales_summary.title}</p>
              <p><strong>Due Date:</strong> {data.sales_summary.due_date}</p>
              <p><strong>Scope Summary:</strong></p>
              <p className="mt-1 text-gray-900">{data.sales_summary.scope_summary}</p>
            </div>
          </section>

          {/* TECHNICAL RESULTS */}
          <section className="p-4 bg-gray-100 rounded-lg shadow border border-gray-300">
            <h2 className="text-xl font-bold text-black">Technical – Spec Match</h2>

            {data.technical.items.length === 0 ? (
              <p className="text-gray-900 text-sm mt-2">No technical items found.</p>
            ) : (
              <div className="space-y-4 mt-2">
                {data.technical.items.map((item: any, idx: number) => (
                  <div key={idx} className="border p-3 bg-white rounded text-gray-900">
                    <p className="font-bold mb-1">
                      RFP Item: <span className="font-normal">{item.rfp_item}</span>
                    </p>

                    {/* SKU MATCH TABLE */}
                    {item.top_matches.length === 0 ? (
                      <p className="text-gray-900 text-sm">No SKU matches found.</p>
                    ) : (
                      <table className="w-full text-sm border mt-2">
                        <thead className="bg-gray-300 text-black">
                          <tr>
                            <th className="border px-2 py-1 text-left">SKU</th>
                            <th className="border px-2 py-1 text-left">Score</th>
                            <th className="border px-2 py-1 text-left">Cores</th>
                            <th className="border px-2 py-1 text-left">Area</th>
                            <th className="border px-2 py-1 text-left">Insulation</th>
                            <th className="border px-2 py-1 text-left">Material</th>
                            <th className="border px-2 py-1 text-left">Voltage</th>
                          </tr>
                        </thead>
                        <tbody>
                          {item.top_matches.map((m: any, j: number) => (
                            <tr key={j} className="text-gray-900">
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
              <thead className="bg-gray-300 text-black">
                <tr>
                  <th className="border px-2 py-1 text-left">RFP Item</th>
                  <th className="border px-2 py-1 text-left">Best SKU</th>
                  <th className="border px-2 py-1 text-left">Match Score</th>
                  <th className="border px-2 py-1 text-left">Total Cost</th>
                </tr>
              </thead>
              <tbody>
                {data.pricing.priced_items.map((p: any, idx: number) => (
                  <tr key={idx} className="text-gray-900">
                    <td className="border px-2 py-1">{p.rfp_item}</td>
                    <td className="border px-2 py-1">{p.best_match_sku}</td>
                    <td className="border px-2 py-1">{p.match_score}</td>
                    <td className="border px-2 py-1">{p.pricing?.total_cost ?? "-"}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </section>
        </section>
      )}
    </main>
  );
}
