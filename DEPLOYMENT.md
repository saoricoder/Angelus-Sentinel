# Vercel Deployment Guide - Angelus Sentinel

## Environment Variables Required

Add these variables to your Vercel dashboard under Project Settings > Environment Variables:

### Firebase Configuration
```
FIREBASE_SERVICE_ACCOUNT_JSON
```
- **Description**: Complete Firebase service account JSON as a string
- **Format**: `{"type": "service_account", "project_id": "...", ...}`
- **How to get**: Download service account key from Firebase Console > Project Settings > Service Accounts

### Gemini API Configuration
```
GEMINI_API_KEY
```
- **Description**: Google Gemini API key for AI processing
- **How to get**: Google AI Studio > Create API Key

### Production Configuration
```
PRODUCTION_URL
```
- **Description**: Your Vercel deployment URL for CORS
- **Format**: `https://your-app-name.vercel.app`
- **Note**: Add after first deployment

### Optional Firebase Config (Alternative to service account)
```
FIREBASE_API_KEY
FIREBASE_AUTH_DOMAIN
FIREBASE_PROJECT_ID
FIREBASE_STORAGE_BUCKET
FIREBASE_MESSAGING_SENDER_ID
FIREBASE_APP_ID
```

## Installation Commands

### 1. Install Vercel CLI
```bash
# Using npm
npm install -g vercel

# Using yarn
yarn global add vercel

# Using pnpm
pnpm add -g vercel
```

### 2. Login to Vercel
```bash
vercel login
```

## Deployment Commands

### First Time Deployment
```bash
# From project root directory
cd c:\Windsuft\Angelus-Sentinel

# Deploy to Vercel
vercel

# Follow prompts:
# - Set up and deploy? [Y/n] y
# - Which scope? [your-account]
# - Link to existing project? [y/N] n
# - What's your project's name? angelus-sentinel
# - In which directory is your code located? ./
```

### Subsequent Deployments
```bash
# Deploy to production
vercel --prod

# Deploy to preview
vercel
```

### Local Development with Vercel
```bash
# Start local development server
vercel dev

# Test API endpoints locally
# Frontend: http://localhost:3000
# Backend API: http://localhost:3000/api/*
```

## Post-Deployment Setup

### 1. Update Production URL
After first deployment, add your Vercel URL to environment variables:
```
PRODUCTION_URL=https://your-app-name.vercel.app
```

### 2. Verify API Endpoints
Test these endpoints in your browser:
- `https://your-app-name.vercel.app/` - API Health Check
- `https://your-app-name.vercel.app/api/patients` - Patients List
- `https://your-app-name.vercel.app/api/notifications` - Notifications

### 3. Monitor Deployment
- Check Vercel dashboard for deployment logs
- Monitor Functions tab for serverless function performance
- Verify environment variables are properly loaded

## Troubleshooting

### Common Issues

**CORS Errors**
- Ensure `PRODUCTION_URL` is set correctly
- Check that your domain is in the allowed origins list

**Firebase Connection Issues**
- Verify `FIREBASE_SERVICE_ACCOUNT_JSON` is properly formatted
- Ensure service account has necessary permissions

**Python Function Timeouts**
- Vercel functions have 10-second timeout for Hobby, 60 for Pro
- Optimize heavy operations or upgrade plan if needed

**Build Failures**
- Check that all dependencies are in `requirements.txt`
- Verify Python version compatibility (3.9-3.11)

### Debug Commands
```bash
# View deployment logs
vercel logs

# Check function performance
vercel inspect

# Test locally with production env
vercel env pull .env.production
vercel dev --env .env.production
```

## Performance Optimization

### Caching Configuration
The `vercel.json` includes optimized caching:
- API routes cached for 60 seconds
- Stale content served while revalidating for 30 seconds

### Recommended Vercel Plan
- **Hobby**: Good for development and light usage
- **Pro**: Recommended for production (longer timeouts, more bandwidth)

## Security Notes

- Never commit `.env` files to version control
- Use Vercel's environment variable encryption
- Regularly rotate API keys
- Monitor Firebase service account permissions
- Enable Vercel's security features (CORS headers, rate limiting)
