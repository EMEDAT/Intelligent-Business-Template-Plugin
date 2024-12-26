// Define the base API URL (for proxying)
const BASE_URL = '/api';

export const fetchConversation = async (platform: string, platformId: string) => {
    const endpoint = `${BASE_URL}/integration/${platform}`;

    try {
        const response = await fetch(endpoint, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                [`${platform === 'slack' ? 'channel_id' : platform === 'teams' ? 'team_id' : 'thread_id'}`]: platformId,
            }),
        });

        if (!response.ok) {
            const errorText = await response.text(); // Get error text from response
            throw new Error(`Failed to fetch conversation: ${response.status} - ${errorText}`);
        }

        return response.json();
    } catch (error) {
        console.error('Error fetching conversation:', error);
        throw error;
    }
};

export const generateTemplate = async (keyPoints: string[], templateType: string, fileFormat: string) => {
    const endpoint = `${BASE_URL}/templates/generate`;
    try {
        const response = await fetch(endpoint, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json', // Keep this for sending the data
            },
            body: JSON.stringify({
                key_points: keyPoints,
                template_type: templateType,
                format: fileFormat,
            }),
        });

        if (!response.ok) {
            const errorText = await response.text();
            throw new Error(`Failed to generate template: ${response.status} - ${errorText}`);
        }

        return response; // Return the full response (crucial for blob handling)
    } catch (error) {
        console.error('Error generating template:', error);
        throw error;
    }
};