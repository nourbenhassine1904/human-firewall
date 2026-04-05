import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Clock, Trash2 } from "lucide-react";

/**
 * HistoryPanel Component
 * Display history of previous analyses
 * Design: Glassmorphism with timeline layout
 */

interface HistoryEntry {
  id: string;
  timestamp: Date;
  message: string;
  prediction: "phishing" | "safe";
  riskScore: number;
}

interface HistoryPanelProps {
  entries: HistoryEntry[];
  onSelect: (entry: HistoryEntry) => void;
  onClear: () => void;
}

export default function HistoryPanel({
  entries,
  onSelect,
  onClear,
}: HistoryPanelProps) {
  if (entries.length === 0) {
    return (
      <div className="p-6 text-center">
        <Clock className="w-8 h-8 text-muted-foreground mx-auto mb-3 opacity-50" />
        <p className="text-sm text-muted-foreground">No analysis history yet</p>
      </div>
    );
  }

  return (
    <div className="p-6 space-y-4">
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-sm font-display text-cyan-400 uppercase tracking-wider">
          Analysis History
        </h3>
        <Button
          onClick={onClear}
          variant="ghost"
          size="sm"
          className="text-muted-foreground hover:text-red-400"
        >
          <Trash2 className="w-4 h-4" />
        </Button>
      </div>

      <div className="space-y-2 max-h-96 overflow-y-auto">
        {entries.map((entry) => (
          <button
            key={entry.id}
            onClick={() => onSelect(entry)}
            className="w-full text-left p-3 rounded-lg glass-card hover:bg-cyan-500/20 hover:border-cyan-500/50 transition-all duration-300 group"
          >
            <div className="flex items-start gap-3">
              <div
                className={`w-2 h-2 rounded-full mt-1.5 flex-shrink-0 ${
                  entry.prediction === "phishing"
                    ? "bg-red-400"
                    : "bg-green-400"
                }`}
              />
              <div className="flex-1 min-w-0">
                <p className="text-xs text-muted-foreground truncate">
                  {entry.message}
                </p>
                <div className="flex items-center justify-between mt-1">
                  <span className="text-xs text-muted-foreground">
                    {entry.timestamp.toLocaleTimeString([], {
                      hour: "2-digit",
                      minute: "2-digit",
                    })}
                  </span>
                  <span
                    className={`text-xs font-mono ${
                      entry.prediction === "phishing"
                        ? "text-red-400"
                        : "text-green-400"
                    }`}
                  >
                    {(entry.riskScore * 100).toFixed(0)}%
                  </span>
                </div>
              </div>
            </div>
          </button>
        ))}
      </div>
    </div>
  );
}
