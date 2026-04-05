import { CheckCircle2 } from "lucide-react";

/**
 * SuccessState Component
 * Display success message after decision submission
 * Design: Green accent with success glow animation
 */

interface SuccessStateProps {
  message: string;
  subMessage?: string;
}

export default function SuccessState({ message, subMessage }: SuccessStateProps) {
  return (
    <div className="flex flex-col items-center justify-center gap-4 p-8 success-glow">
      <div className="p-4 rounded-full bg-green-500/10 border border-green-500/30">
        <CheckCircle2 className="w-8 h-8 text-green-400" />
      </div>
      
      <div className="text-center">
        <p className="text-sm font-display text-green-400 mb-2">
          {message}
        </p>
        {subMessage && (
          <p className="text-xs text-muted-foreground">
            {subMessage}
          </p>
        )}
      </div>
    </div>
  );
}
