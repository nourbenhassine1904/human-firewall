/**
 * LoadingState Component
 * Animated loading indicator for analysis processing
 * Design: Hexagon spinner with cyan glow
 */

export default function LoadingState() {
  return (
    <div className="flex flex-col items-center justify-center gap-4 p-8">
      <div className="relative w-16 h-16">
        {/* Outer rotating ring */}
        <div className="absolute inset-0 rounded-full border-2 border-transparent border-t-cyan-400 border-r-cyan-400 animate-spin" />
        
        {/* Middle pulsing ring */}
        <div className="absolute inset-2 rounded-full border border-cyan-500/30 animate-pulse" />
        
        {/* Inner hexagon */}
        <div className="absolute inset-4 flex items-center justify-center">
          <div className="w-6 h-6 bg-gradient-to-br from-cyan-400 to-magenta-400 rounded-full animate-pulse" />
        </div>
      </div>
      
      <div className="text-center">
        <p className="text-sm font-display text-cyan-400 cyan-glow">
          Analyzing Message
        </p>
        <p className="text-xs text-muted-foreground mt-1">
          Processing with AI model...
        </p>
      </div>
    </div>
  );
}
