import React, { useState } from 'react';
import Header from '../components/Header';
import TemplateCard from '../components/TemplateCard';
import Footer from '../components/Footer';
import styles from '../styles/Home.module.scss';

const Home = () => {
  const [transcript, setTranscript] = useState<string>('');

  const handleTranscriptChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setTranscript(e.target.value);
  };

  return (
    <div className={styles.pageContainer}>
      <Header />
      <main className={styles.mainContent}>
        <h1>Welcome to the Intelligent Business Template Plugin</h1>
        <p>Streamline your business planning with AI-generated templates.</p>
        <div className={styles.inputSection}>
          <input
            type="text"
            value={transcript}
            onChange={handleTranscriptChange}
            placeholder="Paste your conversation transcript here"
            className={styles.inputField}
          />
          <button className={styles.generateButton}>Generate Template</button>
        </div>
        <div className={styles.templates}>
          <TemplateCard
            title="Business Plan Template"
            description="Generate a detailed business plan based on your conversation."
          />
          <TemplateCard
            title="Pitch Deck Template"
            description="Create a professional pitch deck with AI-driven insights."
          />
          <TemplateCard
            title="Marketing Strategy Template"
            description="Build your marketing strategy using AI-suggested approaches."
          />
        </div>
      </main>
      <Footer />
    </div>
  );
};

export default Home;