import { useState } from 'react';
import Header from '../components/Header';
import Footer from '../components/Footer';
import styles from '../styles/Home.module.scss';
import { fetchConversation, generateTemplate } from '../utils/api';

const TemplateGeneration = () => {
    const [platform, setPlatform] = useState('slack');
    const [platformId, setPlatformId] = useState('');
    const [keyPoints, setKeyPoints] = useState<any>(null);
    const [templateType, setTemplateType] = useState('business_plan');
    const [fileFormat, setFileFormat] = useState('word');
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);
    const [keyPointsText, setKeyPointsText] = useState<string>('');
    const [saveOption, setSaveOption] = useState<'download' | 'googleDocs' | null>(null);

    const handlePlatformChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
        setPlatform(e.target.value);
        setPlatformId('');
    };

    const handleFetchConversation = async () => {
        setLoading(true);
        setError(null);
        try {
            if (!platformId) {
                throw new Error("Please enter a Platform ID");
            }
            const response = await fetchConversation(platform, platformId);
            if (response.key_points) {
                setKeyPoints(response.key_points);
                setKeyPointsText(JSON.stringify(response.key_points, null, 2));
            } else {
                throw new Error('No key points found in the conversation. Please provide a more detailed conversation.');
            }
        } catch (err) {
            setError(err instanceof Error ? err.message : 'Failed to fetch conversation');
            setKeyPoints(null);
            setKeyPointsText('');
        } finally {
            setLoading(false);
        }
    };

    const handleGenerateTemplate = async () => {
      setError(null);

      if (!keyPoints) {
          setError('Please fetch a conversation first.');
          return;
      }

      if (!saveOption) {
          setError('Please select a save option (Download or Google Docs).');
          return;
      }

      setLoading(true);

      try {
          if (saveOption === 'googleDocs') {
              const response = await fetch('/api/templates/save_to_google_docs', {
                  method: 'POST',
                  headers: { 'Content-Type': 'application/json' },
                  body: JSON.stringify({ key_points: keyPoints, template_type: templateType }),
              });

              if (!response.ok) {
                  const errorData = await response.json();
                  throw new Error(errorData.error || `Failed to save to Google Docs: ${response.status}`);
              }

              const data = await response.json();
              window.open(data.url, '_blank');
          } else if (saveOption === 'download') {
              try {
                  const response = await generateTemplate(keyPoints, templateType, fileFormat);
                  if (!response) {
                      throw new Error("Failed to generate template on the server.");
                  }
                  const blob = await response.blob();

                  if (!blob) {
                      throw new Error('Failed to generate downloadable content.');
                  }

                  const url = window.URL.createObjectURL(blob);
                  const filename = `${templateType}.${fileFormat}`;

                  const downloadLink = document.createElement('a');
                  downloadLink.href = url;
                  downloadLink.download = filename;
                  downloadLink.style.display = 'none'; // Prevent link from being visible
                  document.body.appendChild(downloadLink); // Append to the document
                  downloadLink.click();
                  document.body.removeChild(downloadLink); // Clean up the link
                  window.URL.revokeObjectURL(url);

                  console.log("Download initiated successfully");
              } catch (downloadError) {
                  console.error("Download Error:", downloadError);
                  setError(downloadError instanceof Error ? downloadError.message : "Download failed");
              }
          }
      } catch (err) {
          setError(err instanceof Error ? err.message : 'An error occurred.');
          console.error("Outer Error:", err);
      } finally {
          setLoading(false);
          setSaveOption(null);
      }
  };

    return (
        <div className={styles.pageContainer}>
            <Header />
            <main className={styles.mainContent}>
                <h1>Generate Your Business Template</h1>

                <div className={styles.inputSection}>
                    <label htmlFor="platform">Select Messaging Platform:</label>
                    <select
                        id="platform"
                        value={platform}
                        onChange={handlePlatformChange}
                        className={styles.selectField}
                    >
                        <option value="slack">Slack</option>
                        <option value="teams">Microsoft Teams</option>
                        <option value="whatsapp">WhatsApp</option>
                    </select>

                    <input
                        type="text"
                        value={platformId}
                        onChange={(e) => setPlatformId(e.target.value)}
                        placeholder={`Enter ${platform === 'slack' ? 'Channel ID' : platform === 'teams' ? 'Team ID' : 'Thread ID'}`}
                        className={styles.inputField}
                    />

                    <button
                        onClick={handleFetchConversation}
                        className={styles.generateButton}
                        disabled={loading || !platformId} // Disable if platform ID is empty
                    >
                        {loading ? 'Fetching...' : 'Fetch Conversation'}
                    </button>
                </div>

                {keyPoints && (
                    <div className={styles.result}>
                        <h2>Key Points</h2>
                        <textarea value={keyPointsText} readOnly className={styles.keyPointsTextarea} />

                        <label htmlFor="templateType">Template Type:</label>
                        <select id="templateType" value={templateType} onChange={(e) => setTemplateType(e.target.value)}>
                            <option value="business_plan">Business Plan</option>
                            <option value="pitch_deck">Pitch Deck</option>
                            <option value="marketing_strategy">Marketing Strategy</option>
                        </select>

                        <div className={styles.saveOptions}>
                            <button
                                onClick={() => setSaveOption('download')}
                                disabled={loading}
                                className={`${styles.saveOptionButton} ${saveOption === 'download' ? styles.activeSaveOption : ''}`}
                            >
                                Download
                            </button>
                            <button
                                onClick={() => setSaveOption('googleDocs')}
                                disabled={loading}
                                className={`${styles.saveOptionButton} ${saveOption === 'googleDocs' ? styles.activeSaveOption : ''}`}
                            >
                                Save to Google Docs
                            </button>
                        </div>

                        {saveOption === 'download' && (
                            <>
                                <label htmlFor="fileFormat">File Format:</label>
                                <select
                                    id="fileFormat"
                                    value={fileFormat}
                                    onChange={(e) => setFileFormat(e.target.value)}
                                    disabled={loading}
                                >
                                    <option value="word">Word (.docx)</option>
                                    <option value="pdf">PDF (.pdf)</option>
                                    <option value="pptx">PowerPoint (.pptx)</option>
                                </select>
                            </>
                        )}

                        <button
                            onClick={handleGenerateTemplate}
                            className={styles.generateButton}
                            disabled={loading || !saveOption}
                        >
                            {loading ? 'Processing...' : 'Generate Template'}
                        </button>
                    </div>
                )}
                {error && <p className={styles.error}>{error}</p>} {/* Error display */}
            </main>
            <Footer />
        </div>
    );
};

export default TemplateGeneration;