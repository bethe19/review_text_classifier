# Sentiment Analysis Frontend

A modern React frontend for the Restaurant Review Sentiment Analysis API.

## Features

- 🎨 Beautiful, modern UI with Tailwind CSS
- 📱 Fully responsive design
- 🔄 Single review analysis
- 📊 Batch review analysis
- ⚡ Fast and responsive
- 🎯 Real-time sentiment prediction with confidence scores

## Prerequisites

- Node.js (v16 or higher)
- npm or yarn
- The FastAPI backend should be running on `http://localhost:8000`

## Installation

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

## Development

Start the development server:

```bash
npm run dev
```

The frontend will be available at `http://localhost:3000`

## Build for Production

Build the production-ready version:

```bash
npm run build
```

The built files will be in the `dist` directory.

Preview the production build:

```bash
npm run preview
```

## Environment Variables

You can configure the API URL by creating a `.env` file:

```env
VITE_API_URL=http://localhost:8000
```

If not set, it defaults to `http://localhost:8000`

## Usage

1. Make sure the FastAPI backend is running
2. Start the frontend development server
3. Open your browser to `http://localhost:3000`
4. Enter a restaurant review and click "Analyze Sentiment"
5. View the results with sentiment (positive/negative) and confidence score

## Features

### Single Review Mode
- Enter one review at a time
- Get instant sentiment analysis
- See confidence percentage

### Batch Mode
- Enter multiple reviews (one per line)
- Analyze all reviews at once
- View results for each review

## Technologies Used

- React 18
- Vite
- Tailwind CSS
- Axios
- Modern ES6+ JavaScript

