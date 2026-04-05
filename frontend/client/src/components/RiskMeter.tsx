/**
 * RiskMeter Component
 * Visual representation of risk score with gradient fill
 * Design: Animated gradient bar from green to red
 */

interface RiskMeterProps {
  score: number; // 0 to 1
}

export default function RiskMeter({ score }: RiskMeterProps) {
  const percentage = Math.min(Math.max(score * 100, 0), 100);

  // Determine color based on score
  let colorClass = "from-green-400 to-green-500";
  if (score > 0.33) colorClass = "from-yellow-400 to-yellow-500";
  if (score > 0.66) colorClass = "from-orange-400 to-orange-500";
  if (score > 0.85) colorClass = "from-red-400 to-red-500";

  return (
    <div className="w-full">
      <div className="relative h-2 bg-background rounded-full overflow-hidden border border-cyan-500/20">
        <div
          className={`h-full bg-gradient-to-r ${colorClass} transition-all duration-500 ease-out`}
          style={{ width: `${percentage}%` }}
        />
        <div
          className="absolute top-0 h-full w-1 bg-white/30 blur-sm"
          style={{ left: `${percentage}%`, transform: "translateX(-50%)" }}
        />
      </div>
    </div>
  );
}
