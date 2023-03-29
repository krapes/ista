import React, { useState } from 'react';
import axios from 'axios';
import ReactLoading from 'react-loading';

function App() {
  const [query, setQuery] = useState('');
  const [response, setResponse] = useState({ response: 'Welcome to Subject Guru. Please ask your first question.' });
  const [loading, setLoading] = useState(false);
  const [uploadStatus, setUploadStatus] = useState({ message: 'Upload' });

  const handleSubmit = async (event) => {
    event.preventDefault();
    setLoading(true);
    setResponse({ response: "!!!!I'm sorry, it looks like there's been a problem" });
    try {
      const { data } = await axios.post('/api/query', { query });
      setResponse(data);
    } catch (error) {
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  const handleFileUpload = async (event) => {
    event.preventDefault();
    const files = event.target.files;
    const formData = new FormData();
    for (let i = 0; i < files.length; i++) {
      formData.append('file', files[i]);
    }
    try {
      await axios.post('/api/fileupload', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      setUploadStatus({ message: 'Upload' });
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
        <button type="submit" style={{ backgroundColor: 'lightgray', color: 'black', padding: '10px', borderRadius: '5px', marginLeft: '10px' }}>Submit</button>
        <label htmlFor="file-upload" style={{ backgroundColor: 'lightgray', color: 'black', padding: '10px', borderRadius: '5px', marginLeft: '10px', cursor: 'pointer' }}>
          {uploadStatus.message}
        </label>
        <input type="file" id="file-upload" onChange={handleFileUpload} multiple style={{ display: 'none' }} />
      </form>
      {loading ? (
        <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', width: '75%', marginTop: '25%' }}>
          <ReactLoading type="spin" color="gray" height={50} width={50} />
        </div>
      ) : (
        response && (
          <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', width: '75%', marginTop: '15%', marginBottom: '25%', border: '5px black', borderRadius: '5px', backgroundColor: 'white' }}>
            <p style={{ textAlign: 'left', width: '100%' }}>{response.response}</p>
          </div>
        )
      )}
    </div>
  );
}

export default App;
