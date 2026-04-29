# Deployment Guide

## Free Deployment Options

### Frontend (Next.js) - Vercel (Recommended)

1. **Setup Vercel Account**
   - Go to [vercel.com](https://vercel.com)
   - Sign up with GitHub

2. **Connect Repository**
   - Import your GitHub repository
   - Vercel will auto-detect Next.js

3. **Environment Variables**
   - Set `NEXT_PUBLIC_API_URL` to your backend URL
   - Example: `https://your-backend.onrender.com`

4. **Deploy**
   - Vercel will automatically build and deploy
   - Your app will be available at `your-app.vercel.app`

### Backend (Python FastAPI) - Render (Recommended)

1. **Setup Render Account**
   - Go to [render.com](https://render.com)
   - Sign up with GitHub

2. **Create Web Service**
   - Choose "Web Service"
   - Connect your GitHub repository
   - Set root path to project directory

3. **Configuration**
   - Runtime: Python 3.9
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python start-backend.py`

4. **Environment Variables**
   - `XAI_API_KEY`: Your Groq API key
   - `XAI_BASE_URL`: `https://api.groq.com/openai/v1`

5. **Deploy**
   - Render will build and deploy
   - Your API will be available at `your-app.onrender.com`

## Alternative Options

### Frontend Alternatives
- **Netlify**: Static export required
- **GitHub Pages**: Free, static only
- **Cloudflare Pages**: Good performance

### Backend Alternatives
- **Railway**: Similar to Render
- **Fly.io**: More complex, Docker-based
- **Heroku**: Limited free tier

## Deployment Checklist

### Pre-deployment
- [ ] Update API URLs in frontend
- [ ] Set environment variables
- [ ] Test build locally
- [ ] Update dependencies

### Post-deployment
- [ ] Test API endpoints
- [ ] Verify frontend-backend connection
- [ ] Monitor performance
- [ ] Set up monitoring

## Environment Variables

### Frontend (.env.local)
```
NEXT_PUBLIC_API_URL=https://your-backend.onrender.com
```

### Backend
```
XAI_API_KEY=your_groq_api_key
XAI_BASE_URL=https://api.groq.com/openai/v1
```

## Troubleshooting

### Common Issues
1. **CORS errors**: Update backend CORS settings
2. **Environment variables**: Ensure proper naming
3. **Build failures**: Check logs for missing dependencies
4. **API timeouts**: Free tiers have limitations

### Performance Tips
1. **Frontend**: Enable caching headers
2. **Backend**: Optimize database queries
3. **Both**: Use CDN for static assets

## Cost Estimation

### Free Tier Limits
- **Vercel**: 100GB bandwidth/month
- **Render**: 750 hours/month (sleeps after 15min)
- **Total**: Completely free for hobby projects

### When to Upgrade
- >1000 users/month
- Need persistent backend
- Require custom domains
- Need better performance

## Streamlit Deployment (Phase 8)

### Streamlit Community Cloud (Recommended)

1. **Setup Streamlit Account**
   - Go to [streamlit.io](https://streamlit.io)
   - Sign up with GitHub

2. **Connect Repository**
   - Create new app from GitHub
   - Set main file path to `streamlit_app.py`
   - Python version: 3.9+

3. **Environment Variables**
   - `XAI_API_KEY`: Your Groq API key
   - `XAI_BASE_URL`: `https://api.groq.com/openai/v1`
   - `DATASET_PATH`: Path to your dataset

4. **Deploy**
   - Streamlit will automatically deploy
   - Your app will be available at `your-app.streamlit.app`

### Local Development

```bash
# Install Streamlit requirements
pip install -r requirements-streamlit.txt

# Run locally
streamlit run streamlit_app.py
```

### Advantages of Streamlit

- **Single file deployment**: No separate frontend/backend
- **Fast prototyping**: Quick development cycle
- **Free hosting**: Streamlit Community Cloud
- **Easy maintenance**: Less complex architecture

### Limitations

- **Less customization**: Limited UI flexibility
- **Performance**: Not optimized for high traffic
- **Scalability**: Single-threaded execution

## Security Considerations

1. **API Keys**: Never expose in frontend
2. **CORS**: Restrict to your domain
3. **HTTPS**: Always use HTTPS
4. **Environment**: Use environment variables for secrets
