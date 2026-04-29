# Frontend UI Generation with Google Stitch and Next.js

## Overview

This document provides a comprehensive prompt for generating frontend UI images and components using Google Stitch, specifically for a restaurant recommendation system built with Next.js framework.

## Google Stitch Prompt for Restaurant Recommendation UI

### **System Prompt**

You are an expert frontend UI/UX designer specializing in modern web applications. Generate high-quality, production-ready UI designs for a restaurant recommendation system using Next.js framework.

### **Application Context**

**Restaurant Recommendation System Features:**
- User preference input form (location, budget, cuisines, rating)
- AI-powered restaurant recommendations with explanations
- Restaurant cards with rich information display
- Loading states and error handling
- Responsive design for mobile and desktop
- Modern, clean interface with good UX

**Tech Stack:**
- **Framework**: Next.js 14+ with App Router
- **Styling**: Tailwind CSS with custom components
- **Icons**: Lucide React or Heroicons
- **State Management**: Zustand or React Context
- **Components**: shadcn/ui component library
- **Typography**: Inter font family
- **Colors**: Modern color scheme with good contrast

### **Design Requirements**

**Visual Style:**
- Clean, modern interface with subtle gradients
- Card-based layouts with proper spacing
- Smooth transitions and micro-interactions
- Professional color palette (primary: blue, secondary: green, accent: orange)
- Consistent border radius (8px for cards, 4px for buttons)
- Proper visual hierarchy with font sizes and weights

**Component Types to Generate:**

1. **Homepage/Landing Page**
   - Hero section with app title and description
   - Quick search bar for location input
   - Featured restaurants or popular cuisines
   - Call-to-action buttons

2. **Input Form Page**
   - Multi-step form with validation
   - Location input with autocomplete suggestions
   - Budget band selector (low/medium/high)
   - Cuisine multi-select with tags
   - Rating slider with visual feedback
   - Additional preferences textarea
   - Submit button with loading states

3. **Results Page**
   - Restaurant recommendation cards
   - Filter and sort options
   - Map view toggle
   - Restaurant detail modal/expandable sections
   - AI explanation panels
   - Pagination or infinite scroll

4. **Restaurant Detail View**
   - Restaurant header with image placeholder
   - Detailed information sections
   - Cuisine tags and dietary information
   - Rating and price information
   - User reviews section
   - Book/Save actions

5. **Loading and Error States**
   - Skeleton loaders for cards
   - Progress indicators
   - Empty state illustrations
   - Error message components
   - Retry buttons

### **Specific UI Elements to Design**

**Form Components:**
- Text inputs with floating labels
- Select dropdowns with custom styling
- Multi-select tag input component
- Range slider for ratings
- Textarea with character count
- Toggle switches for preferences

**Restaurant Cards:**
- Image placeholder (16:9 aspect ratio)
- Restaurant name with typography hierarchy
- Rating stars display
- Price range indicators
- Cuisine tags with pills
- Distance/location information
- Save/favorite buttons
- Expandable AI explanation section

**Navigation and Layout:**
- Sticky header with search
- Sidebar filters (collapsible)
- Breadcrumb navigation
- Footer with links
- Mobile-responsive hamburger menu

**Interactive Elements:**
- Hover states on all clickable elements
- Focus states for accessibility
- Loading spinners and progress bars
- Smooth transitions between states
- Toast notifications for actions

### **Technical Specifications**

**Next.js Structure:**
```
src/
├── app/
│   ├── layout.tsx
│   ├── page.tsx (homepage)
│   ├── search/
│   │   └── page.tsx (input form)
│   ├── results/
│   │   └── page.tsx (results page)
│   └── restaurant/
│       └── [id]/
│           └── page.tsx (detail view)
├── components/
│   ├── ui/
│   │   ├── button.tsx
│   │   ├── input.tsx
│   │   ├── card.tsx
│   │   └── badge.tsx
│   ├── forms/
│   │   ├── preference-form.tsx
│   │   └── search-bar.tsx
│   ├── restaurant/
│   │   ├── restaurant-card.tsx
│   │   ├── restaurant-list.tsx
│   │   └── restaurant-detail.tsx
│   └── layout/
│       ├── header.tsx
│       ├── sidebar.tsx
│       └── footer.tsx
├── lib/
│   ├── utils.ts
│   └── constants.ts
└── styles/
    └── globals.css
```

**Component Library Integration:**
- Use shadcn/ui for base components
- Customize with Tailwind CSS
- Implement consistent design tokens
- Add dark mode support

**Responsive Design:**
- Mobile-first approach
- Breakpoints: sm (640px), md (768px), lg (1024px), xl (1280px)
- Touch-friendly mobile interactions
- Adaptive layouts for different screen sizes

### **Color Scheme and Design Tokens**

**Primary Colors:**
- Primary: #3B82F6 (blue)
- Secondary: #10B981 (green)
- Accent: #F97316 (orange)
- Background: #FFFFFF (white)
- Surface: #F8FAFC (light gray)
- Border: #E2E8F0 (gray)
- Text: #1E293B (dark gray)

**Typography:**
- Font: Inter font family
- Weights: 400 (regular), 500 (medium), 600 (semibold), 700 (bold)
- Sizes: 12px (small), 14px (base), 16px (medium), 18px (large), 24px (xl)

**Spacing:**
- Scale: 4px base unit
- Padding: 4px, 8px, 12px, 16px, 24px, 32px
- Margin: same scale as padding
- Gap: 8px, 12px, 16px

### **User Flow and Interactions**

**Search Flow:**
1. User enters location → autocomplete suggestions appear
2. Select budget band → visual price indicators update
3. Add cuisines → tags appear with remove option
4. Adjust rating slider → real-time value display
5. Submit → loading state with progress indicator
6. Results → smooth transition to results page

**Results Interaction:**
1. Restaurant cards load with staggered animation
2. Hover on cards → subtle elevation and shadow
3. Click restaurant → expand to show AI explanation
4. Filter sidebar → real-time result filtering
5. Sort options → maintain scroll position

**Mobile Considerations:**
- Thumb-friendly touch targets (44px minimum)
- Swipe gestures for card actions
- Collapsible filters to save space
- Bottom navigation for key actions
- Optimized form layouts for mobile keyboards

### **Accessibility Requirements**

**WCAG 2.1 Compliance:**
- Semantic HTML5 structure
- ARIA labels and descriptions
- Keyboard navigation support
- Screen reader compatibility
- Color contrast ratios (4.5:1 minimum)
- Focus indicators visible
- Skip navigation links

**Interactive Elements:**
- All buttons have visible focus states
- Form inputs have proper labels
- Error messages are associated with inputs
- Loading states have aria-live regions
- Modal dialogs have proper focus management

### **Performance Considerations**

**Image Optimization:**
- WebP format with fallbacks
- Responsive image sizing
- Lazy loading for below-fold images
- Placeholder blur effects
- Proper alt text for accessibility

**Animation Performance:**
- CSS transforms for smooth animations
- Reduced motion for accessibility preferences
- 60fps target for transitions
- Hardware acceleration for complex animations

**Bundle Optimization:**
- Code splitting by route
- Dynamic imports for heavy components
- Tree shaking for unused code
- Optimized font loading

### **Specific Image Generation Requests**

**Homepage Hero Section:**
- Modern gradient background with subtle pattern
- App title and tagline
- Search bar with location icon
- Call-to-action button with hover effect
- Background illustration of food/restaurant scene

**Preference Form:**
- Clean form layout with proper spacing
- Floating labels for inputs
- Visual budget band indicators
- Cuisine tag selection interface
- Interactive rating slider
- Submit button with loading state

**Restaurant Cards:**
- Card with subtle shadow and border radius
- Restaurant image placeholder
- Name, rating, price information
- Cuisine tags as pills
- Save/favorite icon buttons
- Expandable AI explanation section

**Loading States:**
- Skeleton loaders for restaurant cards
- Progress bar for form submission
- Spinner with brand colors
- Smooth fade-in animations

**Error States:**
- Friendly error illustrations
- Clear error messages
- Retry buttons with proper styling
- Help links and support information

### **Deliverables Format**

**Image Requirements:**
- High-resolution (2x for retina displays)
- Consistent aspect ratios (16:9 for cards, 1:1 for icons)
- PNG format with transparency
- Optimized file sizes
- Light and dark mode variants

**Component Specifications:**
- Each UI component as separate image
- Hover and focus states shown
- Mobile and desktop variants
- Loading and error states
- Proper spacing and alignment

**Style Guide:**
- Color palette with hex codes
- Typography specifications
- Spacing and sizing rules
- Icon library usage
- Animation timing functions

### **Implementation Notes**

**Next.js Features to Use:**
- App Router for navigation
- Server components for performance
- Image optimization with next/image
- Font optimization with next/font
- Metadata for SEO

**State Management:**
- Zustand for global state
- React Context for theme
- Local storage for preferences
- URL state for search parameters

**API Integration:**
- React Query for data fetching
- Error boundary implementation
- Optimistic updates for better UX
- Caching strategies for performance

This comprehensive prompt will help Google Stitch generate modern, production-ready UI designs for your restaurant recommendation system with Next.js framework.
