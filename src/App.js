import React, { useState } from 'react';
import axios from 'axios';

function App() {
  const [query, setQuery] = useState('');
  const [response, setResponse] = useState('');

  const handleSubmit = async (event) => {
    event.preventDefault();
    try {
      const { data } = await axios.post('/query', { query });
      setResponse(data);
    } catch (error) {
      console.error(error);
    }
  };

  return (
    <div style={{ backgroundColor: 'lightblue', height: '100vh', display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
      <form onSubmit={handleSubmit} style={{ display: 'flex', justifyContent: 'center', marginTop: '25%', width: '75%' }}>
        <input
          type="text"
          value={query}
          onChange={(event) => setQuery(event.target.value)}
          style={{ width: '75%', padding: '10px', border: '1px solid lightgray', borderRadius: '5px' }}
        />
        <button type="submit" style={{ backgroundColor: 'lightgray', color: 'black', padding: '10px', borderRadius: '5px' }}>Submit</button>
      </form>
      {response && (
        <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', width: '75%', marginTop: '25%', border: '5px black', borderRadius: '5px', backgroundColor: 'white' }}>
          <p style={{ textAlign: 'left', width: '100%' }}>{response.response}</p>
        </div>
      )}
    </div>
  );
}

export default App;
