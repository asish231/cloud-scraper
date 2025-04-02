import { useState } from 'react';

export default function Home() {
  const [query, setQuery] = useState('');
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      const res = await fetch(`https://<YOUR_RENDER_BACKEND_URL>/scrape?query=${encodeURIComponent(query)}`);
      const data = await res.json();
      setResult(data.data);
    } catch (error) {
      setResult({ error: 'Failed to fetch data.' });
    }
    setLoading(false);
  };

  return (
    <div style={{ padding: '20px' }}>
      <h1>Dynamic Web Scraper</h1>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Enter topic to scrape"
          required
        />
        <button type="submit">Scrape</button>
      </form>
      {loading && <p>Loading...</p>}
      {result && (
        <div>
          <h2>Scraped Data:</h2>
          <pre>{JSON.stringify(result, null, 2)}</pre>
        </div>
      )}
    </div>
  );
}
