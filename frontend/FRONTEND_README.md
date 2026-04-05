# Human Firewall - Frontend Documentation

## Overview

This is a modern, high-performance React frontend for the **Human Firewall** phishing detection system. The interface combines AI-powered threat analysis with human-in-the-loop validation, featuring a premium cybersecurity command center aesthetic.

## Design Philosophy

**Cybersecurity Command Center** - A futuristic, immersive interface inspired by military command centers and hacker interfaces.

### Color Palette
- **Primary**: Cyan (#00d9ff) - Trust, technology, clarity
- **Secondary**: Neon Magenta (#ff006e) - Urgency, warnings, critical alerts
- **Accent**: Lime Green (#39ff14) - Safety, approved, secure states
- **Background**: Deep Space Black (#0a0e27) - Professional, focused environment

### Typography
- **Display**: Space Mono (monospace) - Technical authority, data readout feel
- **Body**: Outfit (geometric sans-serif) - Modern, readable, professional

### Visual Effects
- Glassmorphism (semi-transparent cards with backdrop blur)
- Neon borders and glowing effects
- Animated threat indicators with pulsing rings
- Smooth fade-in and slide animations
- Grid background pattern for depth

## Project Structure

```
client/
├── src/
│   ├── pages/
│   │   ├── Dashboard.tsx          # Main asymmetric layout
│   │   └── NotFound.tsx           # 404 page
│   ├── components/
│   │   ├── ChatInterface.tsx      # Left panel: message input & chat
│   │   ├── AnalysisDashboard.tsx  # Right panel: analysis results
│   │   ├── RiskMeter.tsx          # Animated risk score visualization
│   │   ├── ThreatIndicators.tsx   # Threat analysis display
│   │   ├── LoadingState.tsx       # Analysis processing animation
│   │   ├── ErrorState.tsx         # Error message display
│   │   ├── SuccessState.tsx       # Success confirmation
│   │   ├── HistoryPanel.tsx       # Analysis history
│   │   └── StatsOverview.tsx      # Overall statistics
│   ├── lib/
│   │   └── types.ts               # TypeScript interfaces
│   ├── contexts/
│   │   └── ThemeContext.tsx       # Theme management
│   ├── App.tsx                    # Main app component
│   ├── index.css                  # Global styles & animations
│   └── main.tsx                   # Entry point
├── index.html                     # HTML template
└── public/                        # Static assets (favicon, etc.)
```

## Key Features

### 1. Asymmetric Layout
- **Left Panel (Chat Interface)**: Message input, demo scenarios, chat history
- **Right Panel (Analysis Dashboard)**: Risk scores, threat indicators, human validation

### 2. Interactive Components
- **Demo Scenarios**: Quick-start buttons for common phishing types
- **Risk Meter**: Animated gradient bar showing threat level
- **Threat Indicators**: Icons and badges for attack types and recommendations
- **Human Decision Panel**: Approve/Reject/Review options with analyst comments

### 3. Real-time Feedback
- Loading animations during API calls
- Error states with retry options
- Success confirmations after decisions
- Smooth transitions between states

### 4. Responsive Design
- Mobile-first approach
- Adapts to various screen sizes
- Touch-friendly interactive elements

## API Integration

The frontend connects to the backend API at `http://localhost:8001` (configurable via `VITE_FRONTEND_FORGE_API_URL`).

### Endpoints Used

**POST /analyze**
```json
Request: { "text": "suspicious message" }
Response: {
  "analysis_id": "uuid",
  "prediction": "phishing|safe",
  "risk_score": 0.85,
  "severity": "high|medium|low",
  "attack_type": "string",
  "explanation": "string",
  "remediation_tips": ["tip1", "tip2"],
  ...
}
```

**POST /decision**
```json
Request: {
  "analysis_id": "uuid",
  "human_decision": "approve|reject|need_review",
  "analyst_comment": "optional comment"
}
Response: { "message": "Decision saved successfully" }
```

## Customization

### Colors
Edit CSS variables in `client/src/index.css`:
```css
:root {
  --primary: #00d9ff;        /* Cyan */
  --secondary: #ff006e;      /* Magenta */
  --accent: #39ff14;         /* Lime Green */
  --background: #0a0e27;     /* Deep Black */
}
```

### Animations
Modify keyframes in `client/src/index.css`:
- `pulse-threat`: Risk indicator pulsing
- `cyan-glow`: Text glow effect
- `fade-in-up`: Entrance animation
- `risk-fill`: Risk meter animation

### Typography
Update font imports in `client/index.html`:
```html
<link href="https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=Outfit:wght@300;400;500;600;700&display=swap" rel="stylesheet" />
```

## Performance Optimizations

- Lazy loading of components
- Memoized callbacks to prevent unnecessary re-renders
- Optimized animations using CSS transforms
- Efficient state management with React hooks
- CDN-hosted generated images for hero sections

## Browser Support

- Chrome/Edge 90+
- Firefox 88+
- Safari 14+
- Mobile browsers (iOS Safari, Chrome Mobile)

## Development

```bash
# Install dependencies
pnpm install

# Start dev server
pnpm dev

# Build for production
pnpm build

# Type checking
pnpm check

# Format code
pnpm format
```

## Deployment

The frontend is deployed as a static site. No backend server is required for the frontend itself—it communicates with the separate backend API.

### Environment Variables

- `VITE_FRONTEND_FORGE_API_URL`: Backend API base URL (default: `http://localhost:8001`)
- `VITE_APP_TITLE`: Application title
- `VITE_APP_LOGO`: Logo URL

## Future Enhancements

1. **Dark/Light Theme Toggle**: Add theme switcher component
2. **Export Reports**: Generate PDF analysis reports
3. **Batch Analysis**: Upload CSV files for bulk analysis
4. **Analytics Dashboard**: Charts showing phishing trends
5. **Multi-language Support**: Internationalization for French/Arabic
6. **Mobile App**: React Native version for mobile devices

## Accessibility

- WCAG 2.1 AA compliant
- Keyboard navigation support
- Screen reader friendly
- High contrast colors for readability
- Focus indicators on interactive elements

## License

Part of the Human Firewall project - AI-powered phishing detection system.
