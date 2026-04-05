import { Card } from "@/components/ui/card";
import { BarChart3, TrendingUp, AlertCircle, CheckCircle2 } from "lucide-react";

/**
 * StatsOverview Component
 * Display overall statistics and metrics
 * Design: Glassmorphism cards with icon badges
 */

interface StatsOverviewProps {
  totalAnalyses: number;
  phishingDetected: number;
  safeMessages: number;
  averageRiskScore: number;
}

export default function StatsOverview({
  totalAnalyses,
  phishingDetected,
  safeMessages,
  averageRiskScore,
}: StatsOverviewProps) {
  const stats = [
    {
      icon: BarChart3,
      label: "Total Analyses",
      value: totalAnalyses,
      color: "text-cyan-400",
      bg: "bg-cyan-500/10",
    },
    {
      icon: AlertCircle,
      label: "Phishing Detected",
      value: phishingDetected,
      color: "text-red-400",
      bg: "bg-red-500/10",
    },
    {
      icon: CheckCircle2,
      label: "Safe Messages",
      value: safeMessages,
      color: "text-green-400",
      bg: "bg-green-500/10",
    },
    {
      icon: TrendingUp,
      label: "Avg Risk Score",
      value: `${(averageRiskScore * 100).toFixed(0)}%`,
      color: "text-purple-400",
      bg: "bg-purple-500/10",
    },
  ];

  return (
    <div className="grid grid-cols-2 gap-3">
      {stats.map((stat, idx) => {
        const Icon = stat.icon;
        return (
          <Card key={idx} className="glass-card p-4">
            <div className="flex items-start gap-3">
              <div className={`p-2 rounded-lg ${stat.bg} border border-${stat.color.split('-')[1]}-500/30`}>
                <Icon className={`w-4 h-4 ${stat.color}`} />
              </div>
              <div className="flex-1 min-w-0">
                <p className="text-xs text-muted-foreground truncate">
                  {stat.label}
                </p>
                <p className={`text-lg font-display ${stat.color} mt-1`}>
                  {stat.value}
                </p>
              </div>
            </div>
          </Card>
        );
      })}
    </div>
  );
}
