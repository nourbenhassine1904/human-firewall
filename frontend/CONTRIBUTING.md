# Contributing to Human Firewall Frontend

## Design System

All contributions should follow the established design system:

### Colors
- **Cyan (#00d9ff)**: Primary actions, information, trust
- **Magenta (#ff006e)**: Warnings, critical alerts, urgency
- **Lime Green (#39ff14)**: Success, safe states, approved
- **Deep Black (#0a0e27)**: Background, professional environment

### Typography
- **Headings**: Space Mono (monospace, 700 weight)
- **Body**: Outfit (geometric sans-serif, 400 weight)
- **Metrics**: Space Mono (monospace, for numerical displays)

### Components
Use existing shadcn/ui components from `client/src/components/ui/`:
- Button, Input, Card, Textarea, Select, Dialog
- Extend with custom variants instead of creating new components

### Animations
- Entrance: 0.6s fade-in-up
- Hover: 0.3s smooth color/scale transitions
- Loading: Pulsing or rotating elements
- Transitions: 0.35s cubic-bezier(0.4, 0, 0.2, 1)

## Code Style

### File Organization
```
component/
├── ComponentName.tsx      # Main component
├── ComponentName.module.css (if needed)
└── index.ts (if exporting from folder)
```

### React Best Practices
```tsx
// ✓ Good: Memoized callbacks, proper dependencies
const handleClick = useCallback(() => {
  // action
}, [dependency]);

// ✗ Avoid: Creating functions in render
const handleClick = () => { /* action */ };
```

### Styling
```tsx
// ✓ Good: Use Tailwind utilities
<div className="flex items-center gap-4 p-6 rounded-lg bg-card border border-cyan-500/30">

// ✗ Avoid: Inline styles or custom CSS
<div style={{ display: 'flex', gap: '16px' }}>
```

## Adding Features

### 1. New Analysis Visualization
1. Create component in `client/src/components/`
2. Import types from `client/src/lib/types.ts`
3. Use existing color and animation utilities
4. Add to `AnalysisDashboard.tsx`

### 2. New Demo Scenario
1. Add to `DEMO_SCENARIOS` array in `ChatInterface.tsx`
2. Include icon emoji, title, description, and message
3. Test with backend API

### 3. New Dashboard Section
1. Create component with glassmorphism styling
2. Add fade-in-up animation class
3. Include in `AnalysisDashboard.tsx` fade-in-up-stagger container

## Testing

### Manual Testing Checklist
- [ ] Component renders without errors
- [ ] All interactive elements respond to clicks
- [ ] Animations are smooth and not janky
- [ ] Colors match design system
- [ ] Text is readable (contrast ratio ≥ 4.5:1)
- [ ] Works on mobile (320px width)
- [ ] Works on desktop (1920px width)

### API Integration Testing
1. Start backend: `python -m uvicorn backend.app.main:app --reload --port 8001`
2. Test each demo scenario
3. Verify error handling
4. Test human decision submission

## Performance Guidelines

### Bundle Size
- Keep component files under 500 lines
- Lazy load heavy components
- Use dynamic imports for routes

### Rendering
- Memoize expensive computations
- Use useCallback for event handlers
- Avoid creating objects in render

### Animations
- Use CSS transforms (not layout properties)
- Limit animation duration to 0.6s max
- Avoid animating too many elements simultaneously

## Accessibility

### Requirements
- Keyboard navigation for all interactive elements
- Focus indicators visible (outline-ring)
- Color not the only indicator of meaning
- ARIA labels for complex components
- Sufficient color contrast (WCAG AA)

### Testing
```bash
# Check accessibility
# Use browser DevTools Lighthouse audit
# Test with keyboard only (no mouse)
# Test with screen reader (NVDA, JAWS, VoiceOver)
```

## Commit Messages

Follow conventional commits:
```
feat: Add risk score visualization component
fix: Correct API URL environment variable
docs: Update deployment guide
style: Improve button hover animation
refactor: Extract common styles to utilities
test: Add component tests
```

## Pull Request Process

1. Create feature branch: `git checkout -b feat/feature-name`
2. Make changes following code style
3. Test thoroughly (manual + automated)
4. Update documentation if needed
5. Commit with conventional messages
6. Push and create PR with description

## Documentation

### Component Documentation
```tsx
/**
 * ComponentName Component
 * Brief description of purpose
 * Design: Style/aesthetic notes
 * 
 * @param prop1 - Description
 * @param prop2 - Description
 */
```

### README Updates
- Update FRONTEND_README.md for major changes
- Document new environment variables
- Add screenshots for UI changes

## Questions?

Refer to:
- [FRONTEND_README.md](./FRONTEND_README.md) - Architecture & features
- [DEPLOYMENT.md](./DEPLOYMENT.md) - Deployment instructions
- [ideas.md](./ideas.md) - Design philosophy
- Original project docs in `/docs/`

## Code Review Criteria

- [ ] Follows design system
- [ ] Uses existing components
- [ ] Proper error handling
- [ ] Performance optimized
- [ ] Accessible
- [ ] Documented
- [ ] Tested
