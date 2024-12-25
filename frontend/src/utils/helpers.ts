// Helper function to format the date
export const formatDate = (date: string): string => {
    const d = new Date(date)
    return d.toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
    })
  }
  
  // Helper function to clean input text (e.g., for removing special characters)
  export const cleanText = (text: string): string => {
    return text.replace(/[^a-zA-Z0-9 ]/g, '')
  }
  
  // Helper function to generate a random ID
  export const generateId = (): string => {
    return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
      const r = (Math.random() * 16) | 0,
        v = c === 'x' ? r : (r & 0x3) | 0x8
      return v.toString(16)
    })
  }
  
  // Helper function to debounce a function (useful for input handling)
  export const debounce = (func: Function, delay: number) => {
    let timer: NodeJS.Timeout
    return function (...args: any) {
      clearTimeout(timer)
      timer = setTimeout(() => func(...args), delay)
    }
  }  