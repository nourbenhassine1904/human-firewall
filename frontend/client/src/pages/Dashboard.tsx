import { useState, useRef, useEffect } from "react";
import ChatInterface from "@/components/ChatInterface";
import AnalysisDashboard from "@/components/AnalysisDashboard";
import { AnalysisResult } from "@/lib/types";

/**
 * Dashboard Component
 * Asymmetric layout: Chat interface on left, Analysis dashboard on right
 * Design: Cybersecurity Command Center with glassmorphism and neon accents
 */

export default function Dashboard() {
  const [analysisResult, setAnalysisResult] = useState<AnalysisResult | null>(null);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const dashboardRef = useRef<HTMLDivElement>(null);

  const handleAnalysis = async (message: string) => {
    setIsAnalyzing(true);
    try {
      // Call backend API
      const response = await fetch(
        `${import.meta.env.VITE_FRONTEND_FORGE_API_URL || "http://127.0.0.1:8001"}/analyze`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ text: message }),
        }
      );

      if (!response.ok) {
        throw new Error(`API error: ${response.statusText}`);
      }

      const data = await response.json();
      setAnalysisResult(data);

      // Scroll to dashboard
      setTimeout(() => {
        dashboardRef.current?.scrollIntoView({ behavior: "smooth" });
      }, 100);
    } catch (error) {
      console.error("Analysis error:", error);
      // Handle error in UI
    } finally {
      setIsAnalyzing(false);
    }
  };

  const handleDecision = async (decision: "approve" | "reject" | "need_review", comment: string) => {
    if (!analysisResult) return;

    try {
      const response = await fetch(
        `${import.meta.env.VITE_FRONTEND_FORGE_API_URL || "http://127.0.0.1:8001"}/decision`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            analysis_id: analysisResult.analysis_id,
            human_decision: decision,
            analyst_comment: comment,
          }),
        }
      );

      if (!response.ok) {
        throw new Error(`Decision error: ${response.statusText}`);
      }

      // Reset analysis after decision
      setTimeout(() => {
        setAnalysisResult(null);
      }, 1500);
    } catch (error) {
      console.error("Decision error:", error);
    }
  };

  return (
    <div className="min-h-screen bg-background grid-bg overflow-hidden">
      {/* Background grid pattern */}
      <div className="fixed inset-0 grid-bg pointer-events-none" />

      {/* Main content container */}
      <div className="relative z-10 h-screen flex">
        {/* Left: Chat Interface */}
        <div className="flex-1 border-r border-cyan-500/20 overflow-hidden flex flex-col">
          <ChatInterface
            onAnalysis={handleAnalysis}
            isAnalyzing={isAnalyzing}
            hasResult={!!analysisResult}
          />
        </div>

        {/* Right: Analysis Dashboard */}
        <div
          ref={dashboardRef}
          className="flex-1 overflow-y-auto overflow-x-hidden flex flex-col"
        >
          {analysisResult ? (
            <AnalysisDashboard
              result={analysisResult}
              onDecision={handleDecision}
              isProcessing={isAnalyzing}
            />
          ) : (
            <div className="flex-1 flex items-center justify-center p-8">
              <div className="text-center">
                <div className="mb-6">
                  <div className="inline-block p-4 rounded-full bg-gradient-to-br from-cyan-500/20 to-magenta-500/20 border border-cyan-500/30">
                    <svg
                      className="w-12 h-12 text-cyan-400"
                      fill="none"
                      stroke="currentColor"
                      viewBox="0 0 24 24"
                    >
                      <path
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        strokeWidth={2}
                        d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"
                      />
                    </svg>
                  </div>
                </div>
                <h2 className="text-2xl font-display text-cyan-400 mb-2">
                  Ready to Analyze
                </h2>
                <p className="text-muted-foreground max-w-xs">
                  Submit a suspicious message on the left to begin threat analysis
                </p>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
