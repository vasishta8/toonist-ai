
import React, { useState } from 'react';
import { fetchPDF } from './Api.jsx';
import './PDFViewer.css';

const handleFetchPDF = async () => {
  setIsLoading(true); // Set loading before fetch
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
  }
  catch (error) {
    setError(error.message);
    console.error('Error fetching PDF:', error);
  }
  finally {
    setIsLoading(false);
  }
};


export default PDFViewer;