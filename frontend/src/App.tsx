import { useState } from 'react'
import AIQuestBuilder from './components/AIQuestBuilder'

function App() {
  // TODO: Получить user_id из аутентификации
  const [userId] = useState('test-user-123')

  return (
    <div style={{ width: '100%', height: '100%' }}>
      <AIQuestBuilder userId={userId} />
    </div>
  )
}

export default App
