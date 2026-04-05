# Human Firewall Frontend - Deployment Guide

## Quick Start

The frontend is ready to deploy as a static site. It requires no backend server—it communicates with the separate Human Firewall backend API.

## Deployment Options

### 1. Manus Platform (Recommended)

Click the **Publish** button in the Manus UI to deploy your frontend with:
- Automatic SSL/TLS certificates
- Global CDN distribution
- Custom domain support
- Analytics and monitoring

### 2. Vercel

```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
vercel
```

### 3. Netlify

```bash
# Build the project
pnpm build

# Deploy using Netlify CLI
netlify deploy --prod --dir=dist
```

### 4. GitHub Pages

```bash
# Update vite.config.ts with base path
# Then build and push to gh-pages branch
pnpm build
git subtree push --prefix dist origin gh-pages
```

### 5. Self-Hosted (Docker)

```dockerfile
FROM node:22-alpine AS builder
WORKDIR /app
COPY package.json pnpm-lock.yaml ./
RUN npm i -g pnpm && pnpm install
COPY . .
RUN pnpm build

FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

## Environment Variables

Set these in your deployment platform:

| Variable | Description | Example |
|----------|-------------|---------|
| `VITE_FRONTEND_FORGE_API_URL` | Backend API endpoint | `https://api.human-firewall.com` |
| `VITE_APP_TITLE` | Application title | `Human Firewall` |
| `VITE_APP_LOGO` | Logo URL | `https://cdn.example.com/logo.png` |
| `VITE_ANALYTICS_ENDPOINT` | Analytics service URL | `https://analytics.example.com` |
| `VITE_ANALYTICS_WEBSITE_ID` | Analytics website ID | `abc123` |

## Pre-Deployment Checklist

- [ ] Backend API is running and accessible
- [ ] `VITE_FRONTEND_FORGE_API_URL` points to correct backend
- [ ] All environment variables are configured
- [ ] Run `pnpm build` locally and test the dist folder
- [ ] Test API connectivity from deployed frontend
- [ ] CORS is properly configured on backend

## Performance Optimization

The frontend includes several optimizations:

1. **Code Splitting**: Automatic route-based code splitting
2. **Image Optimization**: CDN-hosted generated images
3. **CSS Minification**: Tailwind CSS with tree-shaking
4. **JavaScript Minification**: Vite's built-in optimization
5. **Caching**: Static assets with long cache headers

## Monitoring

After deployment, monitor:

1. **API Connectivity**: Check browser console for API errors
2. **Performance**: Use Lighthouse or WebPageTest
3. **Errors**: Monitor error logs in browser DevTools
4. **Analytics**: Track user interactions and feature usage

## Troubleshooting

### "Cannot connect to backend"
- Verify `VITE_FRONTEND_FORGE_API_URL` is correct
- Check CORS headers on backend
- Ensure backend is running and accessible

### "Blank page or 404"
- Check that `dist` folder is being served
- Verify all routes redirect to `index.html` (for SPA routing)
- Check browser console for JavaScript errors

### "Styling looks broken"
- Clear browser cache (Ctrl+Shift+Delete)
- Verify CSS files are being loaded (check Network tab)
- Check for CSP (Content Security Policy) violations

## Rollback

If you need to rollback to a previous version:

1. **On Manus**: Use the Version History in the Management UI
2. **On Vercel**: Revert to previous deployment in Vercel dashboard
3. **On Netlify**: Restore from previous deploy in Netlify UI

## Support

For deployment issues:
1. Check the [FRONTEND_README.md](./FRONTEND_README.md) for configuration details
2. Review error logs in browser DevTools
3. Verify backend API is responding correctly
4. Test API endpoints using curl or Postman

## Security Considerations

1. **HTTPS Only**: Always use HTTPS in production
2. **CORS**: Configure backend CORS to allow frontend domain
3. **API Keys**: Never commit API keys; use environment variables
4. **CSP Headers**: Set Content Security Policy headers
5. **Rate Limiting**: Implement rate limiting on backend API
