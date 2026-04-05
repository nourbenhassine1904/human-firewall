import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Textarea } from "@/components/ui/textarea";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { AlertCircle, CheckCircle2, AlertTriangle, Zap } from "lucide-react";
import { AnalysisResult } from "@/lib/types";
import RiskMeter from "./RiskMeter";
import ThreatIndicators from "./ThreatIndicators";
import { toast } from "sonner";

/**
 * AnalysisDashboard Component
 * Right panel displaying detailed analysis results
 * Design: Glassmorphism, animated risk indicators, threat visualization
 */

interface AnalysisDashboardProps {
  result: AnalysisResult;
  onDecision: (decision: "approve" | "reject" | "need_review", comment: string) => void;
  isProcessing: boolean;
}

export default function AnalysisDashboard({
  result,
  onDecision,
  isProcessing,
}: AnalysisDashboardProps) {
  const [decision, setDecision] = useState<"approve" | "reject" | "need_review" | "">("");
  const [comment, setComment] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);

  const severityConfig = {
    high: {
      icon: AlertCircle,
      color: "text-red-400",
      bg: "bg-red-500/10",
      border: "border-red-500/30",
      label: "🔴 HIGH RISK",
      message: "DO NOT INTERACT",
    },
    medium: {
      icon: AlertTriangle,
      color: "text-yellow-400",
      bg: "bg-yellow-500/10",
      border: "border-yellow-500/30",
      label: "🟠 MEDIUM RISK",
      message: "VERIFY SOURCE",
    },
    low: {
      icon: CheckCircle2,
      color: "text-green-400",
      bg: "bg-green-500/10",
      border: "border-green-500/30",
      label: "🟢 LOW RISK",
      message: "SAFE",
    },
  };

  const config = severityConfig[result.severity];
  const Icon = config.icon;

  const handleDecisionSubmit = async () => {
    if (!decision) {
      toast.error("Please select a decision");
      return;
    }

    setIsSubmitting(true);
    try {
      await onDecision(decision as "approve" | "reject" | "need_review", comment);
      toast.success("Decision saved successfully");
      setDecision("");
      setComment("");
    } catch (error) {
      toast.error("Failed to save decision");
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="flex-1 overflow-y-auto p-6 space-y-6 fade-in-up-stagger">
      {/* Severity Alert */}
      <Card
        className={`${config.bg} ${config.border} border-2 p-6 fade-in-up ${
          result.severity === "high" ? "threat-pulse" : ""
        }`}
      >
        <div className="flex items-start gap-4">
          <Icon className={`w-8 h-8 ${config.color} flex-shrink-0 mt-1`} />
          <div className="flex-1">
            <h2 className={`text-xl font-display ${config.color} mb-1`}>
              {config.label}
            </h2>
            <p className="text-sm text-muted-foreground">{config.message}</p>
          </div>
        </div>
      </Card>

      {/* Risk Score & Key Metrics */}
      <div className="grid grid-cols-2 gap-4 fade-in-up">
        <Card className="glass-card p-6">
          <p className="text-xs text-muted-foreground font-display uppercase tracking-wider mb-3">
            Risk Score
          </p>
          <div className="flex items-end gap-2">
            <span className="text-4xl font-display text-cyan-400">
              {(result.risk_score * 100).toFixed(0)}
            </span>
            <span className="text-sm text-muted-foreground mb-1">%</span>
          </div>
          <RiskMeter score={result.risk_score} />
        </Card>

        <Card className="glass-card p-6">
          <p className="text-xs text-muted-foreground font-display uppercase tracking-wider mb-3">
            Prediction
          </p>
          <div className="flex items-center gap-2">
            <div
              className={`w-3 h-3 rounded-full ${
                result.prediction === "phishing"
                  ? "bg-red-400 animate-pulse"
                  : "bg-green-400"
              }`}
            />
            <span className="text-lg font-display text-foreground capitalize">
              {result.prediction}
            </span>
          </div>
          <p className="text-xs text-muted-foreground mt-3">
            Confidence: {((result.probabilities[result.prediction as keyof typeof result.probabilities] || 0) * 100).toFixed(1)}%
          </p>
        </Card>
      </div>

      {/* Threat Indicators */}
      <ThreatIndicators result={result} />

      {/* Score Breakdown */}
      <Card className="glass-card p-6 fade-in-up">
        <h3 className="text-sm font-display text-cyan-400 uppercase tracking-wider mb-4">
          Score Breakdown
        </h3>
        <div className="space-y-3">
          <div className="flex items-center justify-between">
            <span className="text-sm text-muted-foreground">ML Model Score</span>
            <div className="flex items-center gap-2">
              <div className="w-24 h-2 bg-background rounded-full overflow-hidden">
                <div
                  className="h-full bg-gradient-to-r from-cyan-500 to-cyan-400"
                  style={{ width: `${result.ml_score * 100}%` }}
                />
              </div>
              <span className="text-sm font-mono text-cyan-400 w-12 text-right">
                {(result.ml_score * 100).toFixed(0)}%
              </span>
            </div>
          </div>
          <div className="flex items-center justify-between">
            <span className="text-sm text-muted-foreground">Rules Score</span>
            <div className="flex items-center gap-2">
              <div className="w-24 h-2 bg-background rounded-full overflow-hidden">
                <div
                  className="h-full bg-gradient-to-r from-magenta-500 to-magenta-400"
                  style={{ width: `${result.rules_score * 100}%` }}
                />
              </div>
              <span className="text-sm font-mono text-magenta-400 w-12 text-right">
                {(result.rules_score * 100).toFixed(0)}%
              </span>
            </div>
          </div>
        </div>
      </Card>

      {/* Triggered Rules */}
      {result.rules_triggered.length > 0 && (
        <Card className="glass-card p-6 fade-in-up">
          <h3 className="text-sm font-display text-magenta-400 uppercase tracking-wider mb-4">
            Triggered Rules ({result.rules_triggered.length})
          </h3>
          <div className="space-y-2">
            {result.rules_triggered.map((rule, idx) => (
              <div key={idx} className="flex items-start gap-2 p-2 rounded bg-magenta-500/10 border border-magenta-500/20">
                <Zap className="w-4 h-4 text-magenta-400 flex-shrink-0 mt-0.5" />
                <p className="text-xs text-muted-foreground">{rule}</p>
              </div>
            ))}
          </div>
        </Card>
      )}

      {/* Psychological Analysis */}
      {result.psychological_profile.length > 0 && (
        <Card className="glass-card p-6 fade-in-up">
          <h3 className="text-sm font-display text-purple-400 uppercase tracking-wider mb-3">
            Psychological Manipulation Detected
          </h3>
          <p className="text-sm text-muted-foreground mb-3">
            {result.psychological_explanation}
          </p>
          <div className="space-y-2">
            {result.psychological_profile.map((profile, idx) => (
              <div key={idx} className="text-xs text-muted-foreground flex items-start gap-2">
                <span className="text-purple-400 mt-0.5">•</span>
                <span>{profile}</span>
              </div>
            ))}
          </div>
        </Card>
      )}

      {/* Tunisian Context */}
      {result.tunisian_context_detected && (
        <Card className="glass-card p-6 fade-in-up border-green-500/30">
          <h3 className="text-sm font-display text-green-400 uppercase tracking-wider mb-3">
            🇹🇳 Tunisian Context Detected
          </h3>
          <p className="text-sm text-muted-foreground mb-3">
            {result.tunisian_context_message}
          </p>
          {result.tunisian_indicators.length > 0 && (
            <div className="space-y-2">
              {result.tunisian_indicators.map((indicator, idx) => (
                <div key={idx} className="text-xs text-muted-foreground flex items-start gap-2">
                  <span className="text-green-400 mt-0.5">✓</span>
                  <span>{indicator}</span>
                </div>
              ))}
            </div>
          )}
        </Card>
      )}

      {/* Remediation Tips */}
      {result.remediation_tips.length > 0 && (
        <Card className="glass-card p-6 fade-in-up">
          <h3 className="text-sm font-display text-cyan-400 uppercase tracking-wider mb-4">
            Remediation Tips
          </h3>
          <div className="space-y-2">
            {result.remediation_tips.map((tip, idx) => (
              <div key={idx} className="text-xs text-muted-foreground flex items-start gap-2">
                <span className="text-cyan-400 mt-0.5">→</span>
                <span>{tip}</span>
              </div>
            ))}
          </div>
        </Card>
      )}

      {/* Human Decision Section */}
      <Card className="glass-card p-6 fade-in-up border-cyan-500/50">
        <h3 className="text-sm font-display text-cyan-400 uppercase tracking-wider mb-4">
          Human Validation Required
        </h3>
        <p className="text-xs text-muted-foreground mb-4">
          No action is executed automatically. Please review and provide your decision.
        </p>

        <div className="space-y-4">
          <div>
            <label className="text-xs text-muted-foreground font-display uppercase tracking-wider mb-2 block">
              Your Decision
            </label>
            <Select value={decision} onValueChange={(v) => setDecision(v as any)}>
              <SelectTrigger className="bg-input border-cyan-500/30 text-foreground">
                <SelectValue placeholder="Select decision..." />
              </SelectTrigger>
              <SelectContent className="bg-card border-cyan-500/30">
                <SelectItem value="reject">
                  <span className="text-red-400">🚫 Reject (Phishing)</span>
                </SelectItem>
                <SelectItem value="approve">
                  <span className="text-green-400">✓ Approve (Safe)</span>
                </SelectItem>
                <SelectItem value="need_review">
                  <span className="text-yellow-400">⚠ Need Review</span>
                </SelectItem>
              </SelectContent>
            </Select>
          </div>

          <div>
            <label className="text-xs text-muted-foreground font-display uppercase tracking-wider mb-2 block">
              Analyst Comment (Optional)
            </label>
            <Textarea
              value={comment}
              onChange={(e) => setComment(e.target.value)}
              placeholder="Add your analysis notes..."
              className="bg-input border-cyan-500/30 text-foreground placeholder:text-muted-foreground min-h-24 resize-none"
            />
          </div>

          <Button
            onClick={handleDecisionSubmit}
            disabled={isSubmitting || !decision}
            className="w-full glow-button bg-gradient-to-r from-cyan-500 to-cyan-600 hover:from-cyan-400 hover:to-cyan-500 text-background font-display"
          >
            {isSubmitting ? "Submitting..." : "Submit Decision"}
          </Button>
        </div>
      </Card>

      {/* Analysis ID */}
      <div className="text-center text-xs text-muted-foreground font-mono p-3 rounded bg-background/50 border border-cyan-500/10 fade-in-up">
        <p className="mb-1">Analysis ID</p>
        <p className="text-cyan-400/70 break-all">{result.analysis_id}</p>
      </div>
    </div>
  );
}
