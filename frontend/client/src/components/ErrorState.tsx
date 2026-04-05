import { AlertCircle } from "lucide-react";
import { Button } from "@/components/ui/button";

/**
 * ErrorState Component
 * Display error messages with retry option
 * Design: Red accent with glassmorphism
 */

interface ErrorStateProps {
  message: string;
  onRetry?: () => void;
}

export default function ErrorState({ message, onRetry }: ErrorStateProps) {
  return (
    <div className="flex flex-col items-center justify-center gap-4 p-8">
      <div className="p-4 rounded-full bg-red-500/10 border border-red-500/30">
        <AlertCircle className="w-8 h-8 text-red-400" />
      </div>
      
      <div className="text-center">
        <p className="text-sm font-display text-red-400 mb-2">
          Analysis Error
        </p>
        <p className="text-xs text-muted-foreground max-w-xs">
          {message}
        </p>
      </div>

      {onRetry && (
        <Button
          onClick={onRetry}
          className="mt-2 bg-red-500/20 hover:bg-red-500/30 border border-red-500/50 text-red-400 hover:text-red-300"
          variant="outline"
        >
          Retry
        </Button>
      )}
    </div>
  );
}
