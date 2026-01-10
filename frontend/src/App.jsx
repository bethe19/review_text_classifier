import { useState } from 'react'
import axios from 'axios'
import './App.css'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

function App() {
  const [review, setReview] = useState('')
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState(null)
  const [error, setError] = useState(null)
  const [mode, setMode] = useState('single')
  const [batchReviews, setBatchReviews] = useState('')

  const handleSingleSubmit = async (e) => {
    e.preventDefault()
    if (!review.trim()) {
      setError('Please enter a review')
      return
    }

    setLoading(true)
    setError(null)
    setResult(null)

    try {
      const response = await axios.post(`${API_URL}/predict`, {
        review: review.trim()
      })
      setResult(response.data)
    } catch (err) {
      setError(err.response?.data?.detail || 'An error occurred while predicting sentiment')
    } finally {
      setLoading(false)
    }
  }

  const handleBatchSubmit = async (e) => {
    e.preventDefault()
    const reviews = batchReviews
      .split('\n')
      .map(r => r.trim())
      .filter(r => r.length > 0)

    if (reviews.length === 0) {
      setError('Please enter at least one review')
      return
    }

    setLoading(true)
    setError(null)
    setResult(null)

    try {
      const response = await axios.post(`${API_URL}/predict/batch`, reviews)
      setResult(response.data)
    } catch (err) {
      setError(err.response?.data?.detail || 'An error occurred while predicting sentiment')
    } finally {
      setLoading(false)
    }
  }

  const clearResults = () => {
    setResult(null)
    setError(null)
    setReview('')
    setBatchReviews('')
  }

  const getSentimentColor = (sentiment) => {
    return sentiment === 'positive' ? 'text-orange-600' : 'text-black'
  }

  const getSentimentBgColor = (sentiment) => {
    return sentiment === 'positive' 
      ? 'bg-orange-50 border-orange-300' 
      : 'bg-black border-black'
  }

  const getSentimentTextColor = (sentiment) => {
    return sentiment === 'positive' 
      ? 'text-orange-600' 
      : 'text-black'
  }

  const getConfidenceColor = (confidence) => {
    if (confidence >= 0.8) return 'text-orange-600'
    if (confidence >= 0.6) return 'text-orange-500'
    return 'text-black'
  }

  return (
    <div className="min-h-screen bg-white font-grotesk">
      <div className="container mx-auto px-4 py-12 max-w-5xl">
        <header className="text-center mb-12 border-b-2 border-black pb-8">
          <h1 className="text-5xl font-bold text-black mb-4 tracking-tight">
            RESTAURANT REVIEW SENTIMENT ANALYSIS
          </h1>
          <p className="text-lg text-black font-medium">
            Analyze the sentiment of restaurant reviews using AI
          </p>
        </header>

        <div className="flex justify-center mb-8">
          <div className="bg-white border-2 border-black inline-flex">
            <button
              onClick={() => {
                setMode('single')
                clearResults()
              }}
              className={`px-8 py-3 font-semibold text-sm uppercase tracking-wider transition-all ${
                mode === 'single'
                  ? 'bg-black text-white'
                  : 'text-black hover:bg-black hover:text-white'
              }`}
            >
              Single Review
            </button>
            <button
              onClick={() => {
                setMode('batch')
                clearResults()
              }}
              className={`px-8 py-3 font-semibold text-sm uppercase tracking-wider border-l-2 border-black transition-all ${
                mode === 'batch'
                  ? 'bg-black text-white'
                  : 'text-black hover:bg-black hover:text-white'
              }`}
            >
              Batch Analysis
            </button>
          </div>
        </div>

        <div className="bg-white border-2 border-black p-8 mb-8">
          {mode === 'single' ? (
            <form onSubmit={handleSingleSubmit} className="space-y-6">
              <div>
                <label htmlFor="review" className="block text-sm font-bold text-black mb-3 uppercase tracking-wide">
                  Enter Restaurant Review
                </label>
                <textarea
                  id="review"
                  value={review}
                  onChange={(e) => setReview(e.target.value)}
                  placeholder="e.g., The food was amazing and the service was excellent!"
                  className="w-full px-4 py-4 border-2 border-black bg-white text-black focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-orange-500 resize-none font-grotesk"
                  rows="6"
                />
              </div>
              <button
                type="submit"
                disabled={loading}
                className="w-full bg-orange-600 text-white py-4 px-6 font-bold text-sm uppercase tracking-wider hover:bg-orange-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors border-2 border-black"
              >
                {loading ? 'Analyzing...' : 'Analyze Sentiment'}
              </button>
            </form>
          ) : (
            <form onSubmit={handleBatchSubmit} className="space-y-6">
              <div>
                <label htmlFor="batchReviews" className="block text-sm font-bold text-black mb-3 uppercase tracking-wide">
                  Enter Multiple Reviews (one per line)
                </label>
                <textarea
                  id="batchReviews"
                  value={batchReviews}
                  onChange={(e) => setBatchReviews(e.target.value)}
                  placeholder="Great restaurant!&#10;Terrible food and service&#10;It was okay"
                  className="w-full px-4 py-4 border-2 border-black bg-white text-black focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-orange-500 resize-none font-mono text-sm"
                  rows="8"
                />
              </div>
              <button
                type="submit"
                disabled={loading}
                className="w-full bg-orange-600 text-white py-4 px-6 font-bold text-sm uppercase tracking-wider hover:bg-orange-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors border-2 border-black"
              >
                {loading ? 'Analyzing...' : 'Analyze All Reviews'}
              </button>
            </form>
          )}
        </div>

        {error && (
          <div className="bg-white border-2 border-black p-4 mb-8">
            <div className="flex items-center">
              <span className="text-black mr-3 font-bold">⚠</span>
              <p className="text-black font-medium">{error}</p>
            </div>
          </div>
        )}

        {result && (
          <div className="space-y-6">
            {mode === 'single' ? (
              <div className={`bg-white border-2 border-black p-8 ${result.sentiment === 'positive' ? 'border-orange-600' : ''}`}>
                <div className="flex items-center justify-between mb-6 border-b-2 border-black pb-4">
                  <h2 className="text-3xl font-bold text-black uppercase tracking-tight">Analysis Result</h2>
                  <span className={`text-4xl ${getSentimentTextColor(result.sentiment)}`}>
                    {result.sentiment === 'positive' ? '✓' : '✗'}
                  </span>
                </div>
                
                <div className="space-y-4">
                  <div>
                    <p className="text-xs font-bold text-black mb-2 uppercase tracking-wider">Review:</p>
                    <p className="text-black font-medium">"{result.review}"</p>
                  </div>
                  
                  <div className="flex items-center justify-between pt-4 border-t-2 border-black">
                    <div>
                      <p className="text-xs font-bold text-black mb-2 uppercase tracking-wider">Sentiment:</p>
                      <p className={`text-2xl font-bold uppercase tracking-wide ${getSentimentTextColor(result.sentiment)}`}>
                        {result.sentiment}
                      </p>
                    </div>
                    <div className="text-right">
                      <p className="text-xs font-bold text-black mb-2 uppercase tracking-wider">Confidence:</p>
                      <p className={`text-2xl font-bold ${getConfidenceColor(result.confidence)}`}>
                        {(result.confidence * 100).toFixed(1)}%
                      </p>
                    </div>
                  </div>
                </div>
              </div>
            ) : (
              <div className="bg-white border-2 border-black p-8">
                <h2 className="text-3xl font-bold text-black mb-6 uppercase tracking-tight border-b-2 border-black pb-4">
                  Batch Analysis Results ({result.total} reviews)
                </h2>
                <div className="space-y-4 max-h-96 overflow-y-auto">
                  {result.results.map((item, index) => (
                    <div
                      key={index}
                      className={`p-4 border-2 border-black ${item.sentiment === 'positive' ? 'border-orange-600 bg-orange-50' : 'bg-white'}`}
                    >
                      <div className="flex items-start justify-between mb-3">
                        <span className={`text-lg font-bold uppercase tracking-wide ${getSentimentTextColor(item.sentiment)}`}>
                          {item.sentiment === 'positive' ? '✓' : '✗'} {item.sentiment}
                        </span>
                        <span className={`text-sm font-bold ${getConfidenceColor(item.confidence)}`}>
                          {(item.confidence * 100).toFixed(1)}%
                        </span>
                      </div>
                      <p className="text-sm text-black font-medium">"{item.review}"</p>
                    </div>
                  ))}
                </div>
              </div>
            )}
            
            <button
              onClick={clearResults}
              className="w-full bg-white text-black py-3 px-4 font-bold text-sm uppercase tracking-wider hover:bg-black hover:text-white transition-colors border-2 border-black"
            >
              Clear Results
            </button>
          </div>
        )}
      </div>
    </div>
  )
}

export default App
