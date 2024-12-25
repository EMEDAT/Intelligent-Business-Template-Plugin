// TemplateGeneration.tsx - Updated with Real-Time Suggestions

import React, { useState, useEffect } from 'react';
import Header from '../components/Header';
import Footer from '../components/Footer';
import { generateTemplate } from '../utils/api';
import styles from '../styles/Home.module.scss';

const TemplateGeneration = () => {
  // State variables
  const [transcript, setTranscript] = useState<string>('');
  const [file, setFile] = useState<File | null>(null);
  const [generatedTemplate, setGeneratedTemplate] = useState<string | null>(null);
  const [suggestions, setSuggestions] = useState<string[]>([]);

  // Real-Time Suggestions
  useEffect(() => {
    const socket = new WebSocket('ws://localhost:8000/suggestions');

    socket.onmessage = (event) => {
      const suggestion = JSON.parse(event.data);
      setSuggestions((prev) => [...prev, suggestion.text]);
    };

    return () => {
      socket.close();
    };
  }, []);

  // Handlers
  const handleTranscriptChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setTranscript(e.target.value);
  };

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setFile(e.target.files[0]);
    }
  };

  const handleGenerate = async () => {
    let transcriptData = transcript;

    if (file) {
      const reader = new FileReader();
      reader.onload = async (e) => {
        transcriptData = e.target?.result as string;
        const result = await generateTemplate(transcriptData);
        setGeneratedTemplate(result.template);
      };
      reader.readAsText(file);
    } else {
      const result = await generateTemplate(transcript);
      setGeneratedTemplate(result.template);
    }
  };

  const handleDownload = (format: 'pdf' | 'word' | 'pptx') => {
    if (!generatedTemplate) return;

    fetch(`/api/export?format=${format}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ content: generatedTemplate }),
    })
      .then((response) => response.blob())
      .then((blob) => {
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.style.display = 'none';
        a.href = url;
        a.download = `template.${format}`;
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
      })
      .catch((error) => console.error('Download error:', error));
  };

  return (
    <div className={styles.pageContainer}>
      <Header />
      <main className={styles.mainContent}>
        <h1>Generate Your Business Template</h1>
        <div className={styles.inputSection}>
          <input
            type="text"
            value={transcript}
            onChange={handleTranscriptChange}
            placeholder="Paste conversation transcript here"
            className={styles.inputField}
          />
          <input
            type="file"
            onChange={handleFileChange}
            accept=".txt"
            className={styles.inputField}
          />
          <button onClick={handleGenerate} className={styles.generateButton}>Generate Template</button>
        </div>

        {/* Real-Time Suggestions Section */}
        {suggestions.length > 0 && (
          <div className={styles.suggestionsBox}>
            <h3>Real-Time Suggestions</h3>
            <ul>
              {suggestions.map((suggestion, index) => (
                <li key={index}>{suggestion}</li>
              ))}
            </ul>
          </div>
        )}

        {generatedTemplate && (
          <div className={styles.resultSection}>
            <h2>Generated Template</h2>
            <pre>{generatedTemplate}</pre>
            <div className={styles.exportButtons}>
              <button onClick={() => handleDownload('pdf')} className={styles.exportButton}>Download as PDF</button>
              <button onClick={() => handleDownload('word')} className={styles.exportButton}>Download as Word</button>
              <button onClick={() => handleDownload('pptx')} className={styles.exportButton}>Download as PowerPoint</button>
            </div>
          </div>
        )}
      </main>
      <Footer />
    </div>
  );
};

export default TemplateGeneration;
