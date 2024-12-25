export const generateTemplate = async (transcript: string) => {
    const response = await fetch(`${process.env.API_BASE_URL}/generate-template`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ transcript }),
    })
    const data = await response.json()
    return data
  }
  