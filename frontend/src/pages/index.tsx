import React, { useState } from 'react';
import Header from '../components/Header';
import TemplateCard from '../components/TemplateCard';
import Footer from '../components/Footer';
import styles from '../styles/Home.module.scss';

const Home = () => {
    const [transcript, setTranscript] = useState<string>('');
    const [file, setFile] = useState<File | null>(null);
    const [selectedTemplate, setSelectedTemplate] = useState<string | null>(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);
    const [saveOption, setSaveOption] = useState<'download' | 'googleDocs' | null>(null);

    const handleTranscriptChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        setTranscript(e.target.value);
    };

    const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        if (e.target.files?.length) {
            setFile(e.target.files[0]);
        }
    };

    const handleSelectTemplate = (templateType: string) => {
        setSelectedTemplate(templateType);
    };

    const handleGenerate = async () => {
        setError(null);

        let hasErrors = false;

        if (!selectedTemplate) {
            setError('Please select a template type by clicking "Use Template".');
            hasErrors = true;
        }

        if (!transcript && !file) {
            setError('Please provide a transcript or upload a file.');
            hasErrors = true;
        }

        if (!saveOption) {
            setError('Please select a save option (Download or Google Docs).');
            hasErrors = true;
        }

        if (hasErrors) {
            return;
        }

        setLoading(true);

        try {
            let uploadResponse;
            if (file) {
                const formData = new FormData();
                formData.append('file', file);
                uploadResponse = await fetch('/api/integration/upload', {
                    method: 'POST',
                    body: formData,
                });
            } else if (transcript) {
                uploadResponse = await fetch('/api/integration/upload', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ transcript: transcript }),
                });
            } else {
                throw new Error("No transcript or file to upload"); //Should not happen because of error checking at the beginning of the function
            }

            if (!uploadResponse.ok) {
                const errorText = await uploadResponse.text();
                throw new Error(`Failed to process transcript: ${errorText}`);
            }

            const data = await uploadResponse.json();

            if (saveOption === 'download') {
                const generateResponse = await fetch('/api/templates/generate', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        key_points: data.key_points,
                        template_type: selectedTemplate,
                        format: 'word',
                    }),
                });

                if (!generateResponse.ok) {
                    const errorText = await generateResponse.text();
                    throw new Error(`Failed to generate template: ${errorText}`);
                }

                const blob = await generateResponse.blob();
                const url = window.URL.createObjectURL(blob);
                const link = document.createElement('a');
                link.href = url;

                const contentDisposition = generateResponse.headers.get('Content-Disposition');
                let filename = `${selectedTemplate}.docx`;
                if (contentDisposition) {
                    const filenameMatch = contentDisposition.match(/filename="(.+?)"/);
                    if (filenameMatch) {
                        filename = filenameMatch[1];
                    }
                }

                link.setAttribute('download', filename);
                document.body.appendChild(link);
                link.click();
                link.remove();
                window.URL.revokeObjectURL(url);
            } else if (saveOption === 'googleDocs') {
                const googleDocsResponse = await fetch('/api/templates/save_to_google_docs', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ key_points: data.key_points, template_type: selectedTemplate }),
                });

                if (!googleDocsResponse.ok) {
                    const errorText = await googleDocsResponse.text();
                    throw new Error(`Failed to save to Google Docs: ${errorText}`);
                }

                const googleDocsData = await googleDocsResponse.json();
                window.open(googleDocsData.url, '_blank');
            }
        } catch (err) {
            setError(err instanceof Error ? err.message : 'An unknown error occurred.');
        } finally {
            setLoading(false);
            setSaveOption(null);
        }
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
                    <input
                        type="file"
                        onChange={handleFileChange}
                        className={styles.inputField}
                    />
                    <div className={styles.saveOptions}>
                        <button
                            onClick={() => setSaveOption('download')}
                            className={`${styles.saveOptionButton} ${saveOption === 'download' ? styles.activeSaveOption : ''}`}
                        >
                            Download
                        </button>
                        <button
                            onClick={() => setSaveOption('googleDocs')}
                            className={`${styles.saveOptionButton} ${saveOption === 'googleDocs' ? styles.activeSaveOption : ''}`}
                        >
                            Save to Google Docs
                        </button>
                    </div>
                    <button onClick={handleGenerate} className={styles.generateButton} disabled={loading}>
                        {loading ? 'Processing...' : 'Generate Template'}
                    </button>
                    {error && <p className={styles.error}>{error}</p>}
                </div>
                <div className={styles.templates}>
                    <TemplateCard
                        title="Business Plan Template"
                        description="Generate a detailed business plan based on your conversation."
                        isSelected={selectedTemplate === 'business_plan'}
                        onSelect={() => handleSelectTemplate('business_plan')}
                    />
                    <TemplateCard
                        title="Pitch Deck Template"
                        description="Create a professional pitch deck with AI-driven insights."
                        isSelected={selectedTemplate === 'pitch_deck'}
                        onSelect={() => handleSelectTemplate('pitch_deck')}
                    />
                    <TemplateCard
                        title="Marketing Strategy Template"
                        description="Build your marketing strategy using AI-suggested approaches."
                        isSelected={selectedTemplate === 'marketing_strategy'}
                        onSelect={() => handleSelectTemplate('marketing_strategy')}
                    />
                </div>
            </main>
            <Footer />
        </div>
    );
};

export default Home;