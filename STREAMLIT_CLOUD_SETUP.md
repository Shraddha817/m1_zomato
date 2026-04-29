# Streamlit Cloud Environment Setup

## Required Environment Variables

To deploy the Restaurant Recommender on Streamlit Cloud, you need to set the following environment variables in your app's secrets:

### 1. HF_DATASET_NAME (Required)
```
HF_DATASET_NAME=ManikaSaini/zomato-restaurant-recommendation
```
- **Purpose**: Specifies the Hugging Face dataset to load restaurant data
- **Required**: Yes (for full dataset functionality)
- **Default**: If not set, app will use sample data

### 2. XAI_API_KEY (Optional)
```
XAI_API_KEY=your_groq_api_key_here
```
- **Purpose**: API key for Groq (xAI) LLM service
- **Required**: Only if you want AI-powered recommendations
- **Get from**: https://console.groq.com/keys

### 3. XAI_BASE_URL (Optional)
```
XAI_BASE_URL=https://api.groq.com/openai/v1
```
- **Purpose**: Base URL for Groq API
- **Required**: No (uses default if not set)

### 4. XAI_MODEL (Optional)
```
XAI_MODEL=gemma-7b-it
```
- **Purpose**: Model name for LLM recommendations
- **Required**: No (uses default if not set)

## How to Set Environment Variables in Streamlit Cloud

1. **Go to Streamlit Cloud**: https://share.streamlit.io/
2. **Select your app** or create a new one
3. **Click on "Manage app"** in the lower right corner
4. **Go to "Secrets" tab**
5. **Add the environment variables**:

```toml
HF_DATASET_NAME = "ManikaSaini/zomato-restaurant-recommendation"
XAI_API_KEY = "your_groq_api_key_here"
XAI_BASE_URL = "https://api.groq.com/openai/v1"
XAI_MODEL = "gemma-7b-it"
```

6. **Save and redeploy** your app

## Environment Variable Priority

The app handles missing environment variables gracefully:

1. **HF_DATASET_NAME missing**: Uses sample restaurant data (5 Bangalore restaurants)
2. **XAI_API_KEY missing**: Uses enhanced filtering without AI recommendations
3. **Other variables missing**: Uses sensible defaults

## Testing Environment Variables

You can test environment variables locally by creating a `.env` file:

```bash
# .env file
HF_DATASET_NAME=ManikaSaini/zomato-restaurant-recommendation
XAI_API_KEY=your_groq_api_key_here
XAI_BASE_URL=https://api.groq.com/openai/v1
XAI_MODEL=gemma-7b-it
```

## Troubleshooting

### "HF_DATASET_NAME environment variable not set"
- **Solution**: Add HF_DATASET_NAME to Streamlit Cloud secrets
- **Fallback**: App will use sample data

### "Phase 6 modules not available"
- **Solution**: This is expected on Streamlit Cloud due to import path issues
- **Fallback**: App uses enhanced filtering with scoring

### "No module named 'psutil'"
- **Solution**: Dependencies are now included in requirements-streamlit.txt
- **Action**: Redeploy your app to pick up new dependencies

## Sample Data Mode

When environment variables are not set, the app operates in "Sample Data Mode" with:
- 5 sample restaurants from Bangalore
- Enhanced filtering with scoring
- All UI features functional
- Clear indication that sample data is being used

## Full Feature Mode

With all environment variables set, the app provides:
- Complete restaurant dataset from Hugging Face
- AI-powered recommendations using Groq
- Phase 6 production hardening features
- Full recommendation pipeline
