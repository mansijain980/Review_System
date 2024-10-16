import React, { useState } from 'react';
import axios from 'axios';


function App() {
  const [productUrl, setProductUrl] = useState('');
  const [pageNumber, setPageNumber] = useState('1');
  const [reviews, setReviews] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const fetchReviews = async () => {
    setLoading(true);
    setError('');

    try {
      const response = await axios.get('/api/reviews', {
        params: {
          url: productUrl,
          pageNumber: pageNumber,
        },
      });

      setReviews(response.data.reviews);
      setLoading(false);
    } catch (error) {
      setError('Failed to fetch reviews. Please try again.');
      setLoading(false);
    }
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    fetchReviews();
  };

  return (
    <div style={{padding:'1rem 2rem'}}>
      <h1>Review Scraper</h1>
      <form onSubmit={handleSubmit} style={{display:'flex', flexDirection:'column', gap:'1rem'}}>
        <div style={{gap:'1rem',display:'flex',alignItems:'center'}}>
          <label>Product URL:</label>
          <input
            type="text"
            value={productUrl}
            onChange={(e) => setProductUrl(e.target.value)}
            placeholder="Enter product URL"
            required
            style={{width:'400px',height:'2.5rem',borderRadius:'20px',outline:'none', border:'1px solid lightgray',paddingLeft:'20px'}}
          />
        </div>
        <div style={{gap:'1rem',display:'flex',alignItems:'center'}}>
          <label>Page Number:</label>
          <input
            type="number"
            value={pageNumber}
            onChange={(e) => setPageNumber(e.target.value)}
            placeholder="Page number"
            required
            min="1"
            style={{width:'400px',height:'2.5rem',borderRadius:'20px',outline:'none', border:'1px solid lightgray',paddingLeft:'20px'}}
          />
        </div>
        <button type="submit" style={{height:'2rem', borderRadius:'8px', width:'150px'}}>Scrape Reviews</button>
      </form>

      {loading && <p>Loading reviews...</p>}
      {error && <p style={{ color: 'red' }}>{error}</p>}

      {reviews.length > 0 && (
        <div>
          <h2>Scraped Reviews</h2>
          <ul>
            {reviews.map((review, index) => (
              <li key={index}>
                <h3>{review.title}</h3>
                <p>Rating: {review.rating} stars</p>
                <p>{review.body}</p>
                <p>Reviewer: {review.reviewer}</p>
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}

export default App;
