import { Toaster } from "@/components/ui/sonner";
import { TooltipProvider } from "@/components/ui/tooltip";
import NotFound from "@/pages/NotFound";
import { Route, Switch } from "wouter";
import ErrorBoundary from "./components/ErrorBoundary";
import { ThemeProvider } from "./contexts/ThemeContext";
import Dashboard from "./pages/Dashboard";

/**
 * Design Philosophy: Cybersecurity Command Center
 * - Deep space black background (#0a0e27)
 * - Cyan (#00d9ff) + Magenta (#ff006e) + Lime Green (#39ff14)
 * - Asymmetric layout: Chat left, Analytics right
 * - Glassmorphism + Neon borders
 * - Space Mono for headings, Outfit for body
 */

function Router() {
  return (
    <Switch>
      <Route path={"/"} component={Dashboard} />
      <Route path={"/404"} component={NotFound} />
      {/* Final fallback route */}
      <Route component={NotFound} />
    </Switch>
  );
}

function App() {
  return (
    <ErrorBoundary>
      <div className="dark">
        <ThemeProvider defaultTheme="dark">
          <TooltipProvider>
            <Toaster />
            <Router />
          </TooltipProvider>
        </ThemeProvider>
      </div>
    </ErrorBoundary>
  );
}

export default App;
