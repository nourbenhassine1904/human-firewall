import { useState, useRef, useEffect } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Card } from "@/components/ui/card";
import { Loader2, Send, Zap, Link as LinkIcon, QrCode } from "lucide-react";
import { ChatMessage, DemoScenario } from "@/lib/types";
import LoadingState from "./LoadingState";
import ErrorState from "./ErrorState";

/**
 * ChatInterface Component
 * Left panel with message input and demo scenarios
 * Design: Glassmorphism cards, neon accents, smooth animations
 */

type InputMode = "message" | "url";

const MESSAGE_SCENARIOS: DemoScenario[] = [
  {
    id: "banking",
    title: "Banking Scam",
    description: "Urgent account suspension threat",
    message:
      "Urgent : votre compte BIAT sera suspendu immédiatement. Vérifiez vos informations maintenant via ce lien.",
    icon: "🏦",
  },
  {
    id: "delivery",
    title: "Delivery Scam",
    description: "Package delivery verification",
    message:
      "Votre colis ne peut pas être livré. Merci de confirmer votre adresse avant minuit via ce lien.",
    icon: "📦",
  },
  {
    id: "otp",
    title: "OTP Scam",
    description: "Account security verification",
    message:
      "Votre code OTP est requis pour éviter le blocage de votre compte. Envoyez-le immédiatement.",
    icon: "🔐",
  },
];

const URL_SCENARIOS: DemoScenario[] = [
  {
    id: "url-banking-high",
    title: "Shortened URL (High Risk)",
    description: "Shortened banking phishing link",
    message: "https://bit.ly/biat-verify-account",
    icon: "🔴",
  },
  {
    id: "url-delivery-med",
    title: "Suspicious TLD (Medium Risk)",
    description: "Suspicious domain with .tk TLD",
    message: "https://colis-livraison-urgent.tk/verify",
    icon: "🟠",
  },
  {
    id: "url-legitimate",
    title: "Legitimate Site (Low Risk)",
    description: "Real bank website",
    message: "https://www.biat.com.tn/",
    icon: "🟢",
  },
];

interface ChatInterfaceProps {
  onAnalysis: (message: string) => void;
  isAnalyzing: boolean;
  hasResult: boolean;
}

export default function ChatInterface({
  onAnalysis,
  isAnalyzing,
  hasResult,
}: ChatInterfaceProps) {
  const [message, setMessage] = useState("");
  const [chatHistory, setChatHistory] = useState<ChatMessage[]>([]);
  const [error, setError] = useState<string | null>(null);
  const [mode, setMode] = useState<InputMode>("message");
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [chatHistory]);

  const handleDemoClick = (scenario: DemoScenario) => {
    setMessage(scenario.message);
    // Auto-submit after a short delay
    setTimeout(() => {
      handleSubmit(scenario.message);
    }, 300);
  };

  const handleSubmit = (text?: string) => {
    const messageText = text || message;
    if (!messageText.trim()) return;

    setError(null);

    // Add user message to chat
    const userMessage: ChatMessage = {
      id: `user-${Date.now()}`,
      type: "user",
      content: messageText,
      timestamp: new Date(),
    };

    setChatHistory((prev) => [...prev, userMessage]);
    setMessage("");

    // Trigger analysis
    onAnalysis(messageText);

    // Add bot "analyzing" message
    const botAnalyzingText = mode === "url" 
      ? "🔗 Analyzing URL for phishing indicators..."
      : "🔍 Analyzing message for phishing threats...";
    
    const botMessage: ChatMessage = {
      id: `bot-${Date.now()}`,
      type: "bot",
      content: botAnalyzingText,
      timestamp: new Date(),
    };

    setTimeout(() => {
      setChatHistory((prev) => [...prev, botMessage]);
    }, 300);
  };

  const currentScenarios = mode === "url" ? URL_SCENARIOS : MESSAGE_SCENARIOS;

  return (
    <div className="flex flex-col h-full bg-gradient-to-b from-background via-background to-background/80">
      {/* Header */}
      <div className="border-b border-cyan-500/20 p-6 backdrop-blur-sm">
        <div className="flex items-center gap-3 mb-4">
          <div className="p-2 rounded-lg bg-gradient-to-br from-cyan-500/20 to-magenta-500/20 border border-cyan-500/30">
            <Zap className="w-5 h-5 text-cyan-400" />
          </div>
          <div>
            <h1 className="text-2xl font-display text-cyan-400">Human Firewall</h1>
            <p className="text-xs text-muted-foreground">AI-Powered Phishing Detection</p>
          </div>
        </div>
        
        {/* Mode Toggle */}
        <div className="flex gap-2">
          <button
            onClick={() => { setMode("message"); setChatHistory([]); setMessage(""); }}
            className={`flex-1 flex items-center justify-center gap-2 px-3 py-2 rounded-lg transition-all ${
              mode === "message"
                ? "bg-cyan-500/30 border border-cyan-500/50 text-cyan-300"
                : "glass-card hover:bg-cyan-500/10"
            }`}
          >
            <span className="text-sm">📨 Message</span>
          </button>
          <button
            onClick={() => { setMode("url"); setChatHistory([]); setMessage(""); }}
            className={`flex-1 flex items-center justify-center gap-2 px-3 py-2 rounded-lg transition-all ${
              mode === "url"
                ? "bg-cyan-500/30 border border-cyan-500/50 text-cyan-300"
                : "glass-card hover:bg-cyan-500/10"
            }`}
          >
            <span className="text-sm">🔗 URL/QR</span>
          </button>
        </div>
      </div>

      {/* Chat History */}
      <div className="flex-1 overflow-y-auto p-6 space-y-4">
        {error && <ErrorState message={error} onRetry={() => setError(null)} />}
        {isAnalyzing && chatHistory.length > 0 && <LoadingState />}
        {chatHistory.length === 0 && !isAnalyzing ? (
          <div className="h-full flex flex-col items-center justify-center text-center">
            <div className="mb-6">
              <div className="inline-block p-4 rounded-full bg-gradient-to-br from-cyan-500/10 to-magenta-500/10 border border-cyan-500/20">
                {mode === "url" ? (
                  <LinkIcon className="w-10 h-10 text-cyan-400" />
                ) : (
                  <svg
                    className="w-10 h-10 text-cyan-400"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth={2}
                      d="M13 10V3L4 14h7v7l9-11h-7z"
                    />
                  </svg>
                )}
              </div>
            </div>
            <h2 className="text-lg font-display text-cyan-400 mb-2">
              {mode === "url" ? "Analyze URLs & QR Codes" : "Welcome to Human Firewall"}
            </h2>
            <p className="text-sm text-muted-foreground max-w-xs mb-6">
              {mode === "url"
                ? "Paste a URL or QR code link to check for phishing threats"
                : "Paste a suspicious SMS, email, or message to analyze it for phishing threats"}
            </p>
          </div>
        ) : (
          <>
            {chatHistory.map((msg) => (
              <div
                key={msg.id}
                className={`flex ${msg.type === "user" ? "justify-end" : "justify-start"}`}
              >
                <div
                  className={`message-${msg.type} max-w-xs px-4 py-3 rounded-lg ${
                    msg.type === "user"
                      ? "bg-gradient-to-r from-cyan-500/30 to-cyan-500/10 border border-cyan-500/50 text-cyan-100"
                      : "glass-card text-muted-foreground"
                  }`}
                >
                  <p className="text-sm">{msg.content}</p>
                  <p className="text-xs opacity-50 mt-1">
                    {msg.timestamp.toLocaleTimeString([], {
                      hour: "2-digit",
                      minute: "2-digit",
                    })}
                  </p>
                </div>
              </div>
            ))}
            <div ref={messagesEndRef} />
          </>
        )}
      </div>

      {/* Demo Scenarios */}
      {!hasResult && chatHistory.length === 0 && (
        <div className="px-6 pb-6 space-y-3">
          <p className="text-xs text-muted-foreground font-display uppercase tracking-wider">
            Quick Demo Scenarios
          </p>
          <div className="grid grid-cols-1 gap-2">
            {currentScenarios.map((scenario) => (
              <button
                key={scenario.id}
                onClick={() => handleDemoClick(scenario)}
                disabled={isAnalyzing}
                className="text-left p-3 rounded-lg glass-card hover:bg-cyan-500/20 hover:border-cyan-500/50 transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed group"
              >
                <div className="flex items-center gap-3">
                  <span className="text-lg">{scenario.icon}</span>
                  <div className="flex-1 min-w-0">
                    <p className="text-sm font-medium text-cyan-300 group-hover:text-cyan-200">
                      {scenario.title}
                    </p>
                    <p className="text-xs text-muted-foreground truncate">
                      {scenario.description}
                    </p>
                  </div>
                </div>
              </button>
            ))}
          </div>
        </div>
      )}

      {/* Input Area */}
      <div className="border-t border-cyan-500/20 p-6 backdrop-blur-sm bg-gradient-to-t from-background/40 to-transparent">
        <div className="flex gap-3">
          <Input
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            onKeyPress={(e) => {
              if (e.key === "Enter" && !e.shiftKey) {
                e.preventDefault();
                handleSubmit();
              }
            }}
            placeholder={
              mode === "url"
                ? "Paste a URL or QR code link..."
                : "Paste a suspicious message..."
            }
            className="flex-1 bg-background/50 border-cyan-500/30 focus:border-cyan-400 focus:ring-cyan-400/20"
            disabled={isAnalyzing}
          />
          <Button
            onClick={() => handleSubmit()}
            disabled={isAnalyzing || !message.trim()}
            className="bg-gradient-to-r from-cyan-500/80 to-magenta-500/80 hover:from-cyan-400 hover:to-magenta-400 text-white border-0"
          >
            {isAnalyzing ? (
              <Loader2 className="w-4 h-4 animate-spin" />
            ) : (
              <Send className="w-4 h-4" />
            )}
          </Button>
        </div>
        <p className="text-xs text-muted-foreground mt-2">
          Press Enter to submit • {mode === "url" ? "URLs" : "Messages"} are
          analyzed in real-time
        </p>
      </div>
    </div>
  );
}
