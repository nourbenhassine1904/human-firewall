import { Card } from "@/components/ui/card";
import { AnalysisResult } from "@/lib/types";
import { AlertTriangle, Target, Lightbulb } from "lucide-react";

/**
 * ThreatIndicators Component
 * Display threat analysis details with hexagonal badges
 * Design: Glassmorphism cards with neon accents
 */

interface ThreatIndicatorsProps {
  result: AnalysisResult;
}

export default function ThreatIndicators({ result }: ThreatIndicatorsProps) {
  return (
    <div className="grid grid-cols-1 gap-4 fade-in-up">
      {/* Attack Type */}
      <Card className="glass-card p-6">
        <div className="flex items-start gap-4">
          <div className="p-3 rounded-lg bg-gradient-to-br from-magenta-500/20 to-magenta-500/10 border border-magenta-500/30">
            <Target className="w-5 h-5 text-magenta-400" />
          </div>
          <div className="flex-1">
            <p className="text-xs text-muted-foreground font-display uppercase tracking-wider mb-1">
              Attack Type
            </p>
            <p className="text-sm text-foreground capitalize">{result.attack_type}</p>
          </div>
        </div>
      </Card>

      {/* Recommended Action */}
      <Card className="glass-card p-6">
        <div className="flex items-start gap-4">
          <div className="p-3 rounded-lg bg-gradient-to-br from-cyan-500/20 to-cyan-500/10 border border-cyan-500/30">
            <AlertTriangle className="w-5 h-5 text-cyan-400" />
          </div>
          <div className="flex-1">
            <p className="text-xs text-muted-foreground font-display uppercase tracking-wider mb-1">
              Recommended Action
            </p>
            <p className="text-sm text-foreground">{result.recommended_action}</p>
          </div>
        </div>
      </Card>

      {/* Explanation */}
      <Card className="glass-card p-6">
        <div className="flex items-start gap-4">
          <div className="p-3 rounded-lg bg-gradient-to-br from-purple-500/20 to-purple-500/10 border border-purple-500/30">
            <Lightbulb className="w-5 h-5 text-purple-400" />
          </div>
          <div className="flex-1">
            <p className="text-xs text-muted-foreground font-display uppercase tracking-wider mb-2">
              AI Explanation
            </p>
            <p className="text-sm text-muted-foreground leading-relaxed">
              {result.explanation}
            </p>
          </div>
        </div>
      </Card>
    </div>
  );
}
