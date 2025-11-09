/**
 * QuestLibrary - модальное окно для загрузки существующих квестов
 */
import { useState, useEffect } from 'react'
import axios from 'axios'
import { QuestGraph } from '../../types/quest'

interface Quest {
  id: string
  title: string
  location: string
  difficulty: string
  psychological_module: string
  graph_structure: QuestGraph
  rating: number
  plays_count: number
}

interface Props {
  isOpen: boolean
  onClose: () => void
  onSelectQuest: (graph: QuestGraph, title: string) => void
}

export default function QuestLibrary({ isOpen, onClose, onSelectQuest }: Props) {
  const [quests, setQuests] = useState<Quest[]>([])
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  // Загрузить квесты при открытии модального окна
  useEffect(() => {
    if (isOpen) {
      loadQuests()
    }
  }, [isOpen])

  const loadQuests = async () => {
    setIsLoading(true)
    setError(null)

    try {
      const response = await axios.get('/api/quests/existing')
      setQuests(response.data)
    } catch (err: any) {
      console.error('Error loading quests:', err)
      setError(err.response?.data?.detail || 'Ошибка загрузки квестов')
    } finally {
      setIsLoading(false)
    }
  }

  const handleSelectQuest = (quest: Quest) => {
    onSelectQuest(quest.graph_structure, quest.title)
    onClose()
  }

  if (!isOpen) return null

  return (
    <div style={{
      position: 'fixed',
      top: 0,
      left: 0,
      right: 0,
      bottom: 0,
      background: 'rgba(0, 0, 0, 0.5)',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      zIndex: 1000
    }}>
      <div style={{
        background: 'white',
        borderRadius: '12px',
        padding: '30px',
        maxWidth: '700px',
        width: '90%',
        maxHeight: '80vh',
        overflow: 'auto',
        boxShadow: '0 10px 40px rgba(0, 0, 0, 0.2)'
      }}>
        <div style={{
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center',
          marginBottom: '20px'
        }}>
          <h2 style={{ margin: 0, fontSize: '24px' }}>Библиотека квестов</h2>
          <button
            onClick={onClose}
            style={{
              background: 'transparent',
              border: 'none',
              fontSize: '28px',
              cursor: 'pointer',
              color: '#666'
            }}
          >
            ×
          </button>
        </div>

        {error && (
          <div style={{
            background: '#fef2f2',
            border: '1px solid #fecaca',
            borderRadius: '8px',
            padding: '12px',
            marginBottom: '20px',
            color: '#991b1b'
          }}>
            {error}
          </div>
        )}

        {isLoading ? (
          <div style={{ textAlign: 'center', padding: '40px', color: '#666' }}>
            Загрузка квестов...
          </div>
        ) : quests.length === 0 ? (
          <div style={{
            textAlign: 'center',
            padding: '40px',
            color: '#666'
          }}>
            <p style={{ marginBottom: '20px' }}>Квесты еще не загружены</p>
            <button
              onClick={async () => {
                try {
                  await axios.post('/api/quests/load_yaml_quests')
                  await loadQuests()
                } catch (err) {
                  setError('Ошибка загрузки YAML квестов')
                }
              }}
              style={{
                padding: '10px 20px',
                background: '#3b82f6',
                color: 'white',
                border: 'none',
                borderRadius: '8px',
                cursor: 'pointer',
                fontSize: '14px'
              }}
            >
              Загрузить квесты из YAML
            </button>
          </div>
        ) : (
          <div style={{ display: 'flex', flexDirection: 'column', gap: '15px' }}>
            {quests.map(quest => (
              <div
                key={quest.id}
                onClick={() => handleSelectQuest(quest)}
                style={{
                  border: '1px solid #e5e7eb',
                  borderRadius: '8px',
                  padding: '15px',
                  cursor: 'pointer',
                  transition: 'all 0.2s',
                  ':hover': {
                    borderColor: '#3b82f6',
                    background: '#f9fafb'
                  }
                }}
                onMouseEnter={(e) => {
                  e.currentTarget.style.borderColor = '#3b82f6'
                  e.currentTarget.style.background = '#f9fafb'
                }}
                onMouseLeave={(e) => {
                  e.currentTarget.style.borderColor = '#e5e7eb'
                  e.currentTarget.style.background = 'white'
                }}
              >
                <h3 style={{ margin: '0 0 8px 0', fontSize: '18px' }}>
                  {quest.title}
                </h3>
                <div style={{
                  display: 'flex',
                  gap: '10px',
                  flexWrap: 'wrap',
                  fontSize: '12px',
                  color: '#666'
                }}>
                  <span style={{
                    background: '#dbeafe',
                    padding: '4px 8px',
                    borderRadius: '4px'
                  }}>
                    📍 {quest.location}
                  </span>
                  <span style={{
                    background: getDifficultyColor(quest.difficulty),
                    padding: '4px 8px',
                    borderRadius: '4px'
                  }}>
                    {getDifficultyLabel(quest.difficulty)}
                  </span>
                  <span style={{
                    background: '#e5e7eb',
                    padding: '4px 8px',
                    borderRadius: '4px'
                  }}>
                    ⭐ {quest.rating.toFixed(1)}
                  </span>
                  <span style={{
                    background: '#e5e7eb',
                    padding: '4px 8px',
                    borderRadius: '4px'
                  }}>
                    🎮 {quest.plays_count} прохождений
                  </span>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}

function getDifficultyColor(difficulty: string): string {
  switch (difficulty) {
    case 'easy': return '#dcfce7'
    case 'medium': return '#fef9c3'
    case 'hard': return '#fee2e2'
    default: return '#e5e7eb'
  }
}

function getDifficultyLabel(difficulty: string): string {
  switch (difficulty) {
    case 'easy': return '🟢 Легко'
    case 'medium': return '🟡 Средне'
    case 'hard': return '🔴 Сложно'
    default: return difficulty
  }
}
