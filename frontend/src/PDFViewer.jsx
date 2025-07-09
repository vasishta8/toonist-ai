
import React, { useState } from 'react';
import './PDFViewer.css';

const PDFViewer = () => {
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [pdfUrl, setPdfUrl] = useState('');

  const handleFetchPDF = async () => {
    setIsLoading(true);
    setError(null);
    try {
      const res = await fetch("http://127.0.0.1:5000/fetch_pdf", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
      });
      const data = await res.json();
      if (res.ok) {
        setPdfUrl(data.pdf_url);
      } else {
        throw new Error(data.error || 'Failed to fetch PDF');
      }
    } catch (error) {
      setError(error.message);
      console.error('Error fetching PDF:', error);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="pdf-viewer-container">
      <button onClick={handleFetchPDF} disabled={isLoading}>
        {isLoading ? 'Loading...' : 'Fetch PDF'}
      </button>
      {error && <div className="error">{error}</div>}
      {pdfUrl && (
        <iframe src={pdfUrl} width="100%" height="600px" title="PDF Viewer" />
      )}
    </div>
  );
};

export default PDFViewer;