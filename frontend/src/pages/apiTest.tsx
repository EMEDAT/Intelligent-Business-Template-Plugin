import React, { useEffect, useState } from 'react'

const ApiTest = () => {
  const [response, setResponse] = useState<any>(null)

  useEffect(() => {
    const fetchData = async () => {
      const res = await fetch('/api/test-endpoint')
      const data = await res.json()
      setResponse(data)
    }
    fetchData()
  }, [])

  return (
    <div>
      <h1>API Test</h1>
      <pre>{JSON.stringify(response, null, 2)}</pre>
    </div>
  )
}

export default ApiTest