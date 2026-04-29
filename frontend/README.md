# Restaurant Recommendation Frontend

## Overview

Modern React frontend built with Next.js 14 and Tailwind CSS for the restaurant recommendation system.

## Features

- 🍽️ **Smart Recommendations**: AI-powered restaurant suggestions
- 📍 **Location-based**: Filter by area and proximity
- 💰 **Budget Filtering**: Low/Medium/High budget bands
- 🍴 **Cuisine Selection**: Multi-select cuisine preferences
- ⭐ **Rating Filters**: Minimum rating requirements
- 🔄 **Real-time Updates**: Live API integration
- 📱 **Responsive Design**: Mobile and desktop optimized
- ♿ **Accessibility**: WCAG 2.1 compliant

## Tech Stack

- **Framework**: Next.js 14 with App Router
- **Styling**: Tailwind CSS with custom components
- **Icons**: Lucide React
- **TypeScript**: Full type safety
- **API Integration**: RESTful API to Phase 6 backend

## Quick Start

### Prerequisites
- Node.js 18+
- npm or yarn

### Installation
```bash
cd frontend
npm install
```

### Development
```bash
# Start development server
npm run dev

# Open http://localhost:3000
```

### Production
```bash
# Build for production
npm run build

# Start production server
npm start
```

## Run Both Frontend and Backend

### Option 1: Concurrent Development
```bash
# Terminal 1: Start backend
cd e:\NextLeap\Milestone_1
python -m uvicorn src.milestone1.phase6_hardening.production:app --host 0.0.0.0 --port 8000

# Terminal 2: Start frontend
cd e:\NextLeap\Milestone_1\frontend
npm run dev
```

### Option 2: Development Scripts
```bash
# Create start script
npm run start:all
```

## API Integration

The frontend communicates with Phase 6 hardened backend through REST API:

### Endpoints
- `POST /api/recommendations` - Submit preferences and get recommendations
- `GET /api/locations` - Get available locations
- `GET /api/restaurants/:id` - Get restaurant details
- `GET /api/health` - Health check

### Request/Response Format
```typescript
// Request
interface UserPreferences {
  location: string
  budgetBand?: string
  cuisines?: string[]
  minRating?: number
  additionalPreferences?: string
}

// Response
interface Recommendation {
  restaurant: Restaurant
  rank: number
  explanation: string
}
```

## Project Structure

```
frontend/
├── src/
│   ├── app/
│   │   ├── layout.tsx
│   │   ├── page.tsx (homepage)
│   │   ├── preferences/
│   │   │   └── page.tsx
│   │   └── results/
│   │       └── page.tsx
│   ├── components/
│   │   ├── ui/
│   │   ├── forms/
│   │   ├── restaurant/
│   │   └── layout/
│   ├── lib/
│   │   ├── api.ts
│   │   └── utils.ts
│   └── styles/
│       └── globals.css
├── package.json
├── next.config.js
├── tailwind.config.js
└── README.md
```

## Environment Variables

Create `.env.local` in frontend directory:

```bash
NEXT_PUBLIC_API_URL=http://localhost:8000/api
NEXT_PUBLIC_APP_NAME=Restaurant Recommender
```

## Features

### Homepage
- Hero section with app title
- Quick search functionality
- Feature highlights
- Call-to-action buttons

### Preferences Form
- Location input with autocomplete
- Budget band selector (Low/Medium/High)
- Multi-select cuisine tags
- Rating slider (1.0-5.0)
- Additional preferences textarea
- Form validation and error handling

### Results Page
- Restaurant cards with rich information
- AI explanations for each recommendation
- Filter and sort options
- Loading states and error handling
- Empty state handling

### Responsive Design
- Mobile-first approach
- Breakpoints: sm(640px), md(768px), lg(1024px), xl(1280px)
- Touch-friendly interactions

## Development Notes

### API Integration
- Uses `fetch` API for backend communication
- Error handling with fallback UI
- Loading states during API calls
- Type-safe API interfaces

### State Management
- React hooks for local state
- URL parameters for search state
- LocalStorage for user preferences

### Styling
- Tailwind CSS utility classes
- Custom component variants
- Consistent design tokens
- Dark mode support (planned)

## Testing

```bash
# Run type checking
npm run type-check

# Run linter
npm run lint

# Build and test
npm run build
```

## Deployment

### Local Development
```bash
# Frontend: http://localhost:3000
# Backend: http://localhost:8000
```

### Production Build
```bash
npm run build
# Output: .next/dist/
```

## Troubleshooting

### Common Issues

1. **API Connection Failed**
   - Check backend is running on port 8000
   - Verify API_URL in .env.local
   - Check CORS settings

2. **Build Errors**
   - Run `npm run type-check`
   - Check TypeScript configuration
   - Verify import paths

3. **Styling Issues**
   - Check Tailwind CSS configuration
   - Verify custom CSS classes
   - Clear browser cache

### Getting Help

- Check browser console for errors
- Review network tab in dev tools
- Verify API responses in Network tab
- Check backend logs for API issues

## Contributing

1. Follow TypeScript and React best practices
2. Use semantic HTML5 elements
3. Implement proper error boundaries
4. Test on mobile and desktop
5. Follow WCAG accessibility guidelines

## License

MIT License - see LICENSE file for details
