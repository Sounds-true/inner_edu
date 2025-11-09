/**
 * AIQuestBuilder - главный компонент для создания квестов
 * Левая панель: чат с AI
 * Центр: React Flow граф
 * Правая панель: редактор узла (опционально)
 */
import { useState, useCallback, useEffect } from 'react'
import ReactFlow, {
  Node,
  Edge,
  Controls,
  Background,
  MiniMap,
  useNodesState,
  useEdgesState,
  addEdge,
  Connection,
  BackgroundVariant,
} from 'reactflow'
import 'reactflow/dist/style.css'
import { QuestGraph, ChatMessage } from '../../types/quest'
import axios from 'axios'
import QuestLibrary from './QuestLibrary'

interface Props {
  userId: string
}

export default function AIQuestBuilder({ userId }: Props) {
  const [nodes, setNodes, onNodesChange] = useNodesState([])
  const [edges, setEdges, onEdgesChange] = useEdgesState([])

  const [sessionId, setSessionId] = useState<string | null>(null)
  const [messages, setMessages] = useState<ChatMessage[]>([])
  const [inputMessage, setInputMessage] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [currentStage, setCurrentStage] = useState('')
  const [isLibraryOpen, setIsLibraryOpen] = useState(false)
  const [questTitle, setQuestTitle] = useState('')

  // Отправить сообщение в чат
  const sendMessage = async () => {
    if (!inputMessage.trim() || isLoading) return

    const userMessage: ChatMessage = {
      role: 'user',
      content: inputMessage
    }

    setMessages(prev => [...prev, userMessage])
    setInputMessage('')
    setIsLoading(true)

    try {
      const response = await axios.post('/api/builder/chat', {
        user_id: userId,
        message: inputMessage,
        session_id: sessionId
      })

      const aiMessage: ChatMessage = {
        role: 'assistant',
        content: response.data.ai_response
      }

      setMessages(prev => [...prev, aiMessage])
      setSessionId(response.data.session_id)
      setCurrentStage(response.data.stage)

      // Если AI сгенерировал граф
      if (response.data.graph) {
        updateGraphFromBackend(response.data.graph)
      }

    } catch (error) {
      console.error('Error sending message:', error)
      const errorMessage: ChatMessage = {
        role: 'assistant',
        content: 'Извини, произошла ошибка. Попробуй еще раз.'
      }
      setMessages(prev => [...prev, errorMessage])
    } finally {
      setIsLoading(false)
    }
  }

  // Обновить граф из данных backend
  const updateGraphFromBackend = (graph: QuestGraph) => {
    if (!graph || !graph.nodes) return

    // Конвертировать nodes в React Flow формат
    const flowNodes: Node[] = graph.nodes.map(node => ({
      id: node.id,
      type: node.type,
      position: node.position,
      data: {
        label: getNodeLabel(node),
        ...node.data
      }
    }))

    // Конвертировать edges
    const flowEdges: Edge[] = graph.edges.map(edge => ({
      id: edge.id,
      source: edge.source,
      target: edge.target,
      label: edge.label,
      animated: edge.animated || false
    }))

    setNodes(flowNodes)
    setEdges(flowEdges)
  }

  // Загрузить квест из библиотеки
  const handleLoadQuest = (graph: QuestGraph, title: string) => {
    setQuestTitle(title)
    updateGraphFromBackend(graph)

    const loadMessage: ChatMessage = {
      role: 'assistant',
      content: `Загрузил квест "${title}". Можешь редактировать узлы или попросить меня изменить что-то.`
    }
    setMessages(prev => [...prev, loadMessage])
  }

  // Получить label для узла
  const getNodeLabel = (node: any): string => {
    switch (node.type) {
      case 'start':
        return node.data.title || 'Начало'
      case 'questStep':
        return node.data.dialogue?.substring(0, 30) + '...' || 'Шаг квеста'
      case 'choice':
        return node.data.question || 'Выбор'
      case 'realityBridge':
        return 'Reality Bridge: ' + (node.data.description?.substring(0, 20) || '')
      case 'end':
        return 'Конец'
      default:
        return 'Узел'
    }
  }

  // Обработка новых связей (если родитель добавляет вручную)
  const onConnect = useCallback(
    (params: Connection) => setEdges((eds) => addEdge(params, eds)),
    [setEdges]
  )

  // Начальное приветствие
  useEffect(() => {
    const greetingMessage: ChatMessage = {
      role: 'assistant',
      content: 'Привет! Давай создадим квест для твоего ребенка. Расскажи, чему ты хочешь его научить?'
    }
    setMessages([greetingMessage])
  }, [])

  return (
    <div style={{ display: 'flex', width: '100%', height: '100%' }}>
      {/* Модальное окно библиотеки квестов */}
      <QuestLibrary
        isOpen={isLibraryOpen}
        onClose={() => setIsLibraryOpen(false)}
        onSelectQuest={handleLoadQuest}
      />

      {/* Левая панель: Чат */}
      <div style={{
        width: '350px',
        borderRight: '1px solid #ccc',
        display: 'flex',
        flexDirection: 'column',
        background: '#f9fafb'
      }}>
        <div style={{
          padding: '20px',
          borderBottom: '1px solid #ccc',
          background: '#3b82f6',
          color: 'white'
        }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <div>
              <h2 style={{ margin: 0, fontSize: '20px' }}>AI Quest Builder</h2>
              {currentStage && (
                <p style={{ margin: '5px 0 0 0', fontSize: '12px', opacity: 0.9 }}>
                  Стадия: {currentStage}
                </p>
              )}
              {questTitle && (
                <p style={{ margin: '5px 0 0 0', fontSize: '11px', opacity: 0.8 }}>
                  📖 {questTitle}
                </p>
              )}
            </div>
            <button
              onClick={() => setIsLibraryOpen(true)}
              style={{
                background: 'rgba(255, 255, 255, 0.2)',
                border: 'none',
                borderRadius: '6px',
                padding: '8px 12px',
                color: 'white',
                cursor: 'pointer',
                fontSize: '20px',
                transition: 'background 0.2s'
              }}
              onMouseEnter={(e) => e.currentTarget.style.background = 'rgba(255, 255, 255, 0.3)'}
              onMouseLeave={(e) => e.currentTarget.style.background = 'rgba(255, 255, 255, 0.2)'}
              title="Загрузить квест из библиотеки"
            >
              📚
            </button>
          </div>
        </div>

        {/* Сообщения */}
        <div style={{
          flex: 1,
          overflowY: 'auto',
          padding: '20px',
          display: 'flex',
          flexDirection: 'column',
          gap: '15px'
        }}>
          {messages.map((msg, idx) => (
            <div
              key={idx}
              style={{
                alignSelf: msg.role === 'user' ? 'flex-end' : 'flex-start',
                maxWidth: '80%',
                padding: '10px 15px',
                borderRadius: '12px',
                background: msg.role === 'user' ? '#3b82f6' : '#e5e7eb',
                color: msg.role === 'user' ? 'white' : 'black'
              }}
            >
              {msg.content}
            </div>
          ))}
          {isLoading && (
            <div style={{ alignSelf: 'flex-start', color: '#6b7280' }}>
              AI думает...
            </div>
          )}
        </div>

        {/* Поле ввода */}
        <div style={{
          padding: '15px',
          borderTop: '1px solid #ccc',
          background: 'white'
        }}>
          <div style={{ display: 'flex', gap: '10px' }}>
            <input
              type="text"
              value={inputMessage}
              onChange={(e) => setInputMessage(e.target.value)}
              onKeyPress={(e) => e.key === 'Enter' && sendMessage()}
              placeholder="Напиши сообщение..."
              disabled={isLoading}
              style={{
                flex: 1,
                padding: '10px',
                border: '1px solid #d1d5db',
                borderRadius: '8px',
                fontSize: '14px'
              }}
            />
            <button
              onClick={sendMessage}
              disabled={isLoading || !inputMessage.trim()}
              style={{
                padding: '10px 20px',
                background: '#3b82f6',
                color: 'white',
                border: 'none',
                borderRadius: '8px',
                cursor: isLoading ? 'not-allowed' : 'pointer',
                opacity: isLoading || !inputMessage.trim() ? 0.5 : 1
              }}
            >
              ➤
            </button>
          </div>
        </div>
      </div>

      {/* Центр: React Flow граф */}
      <div style={{ flex: 1, background: '#fafafa' }}>
        {nodes.length > 0 ? (
          <ReactFlow
            nodes={nodes}
            edges={edges}
            onNodesChange={onNodesChange}
            onEdgesChange={onEdgesChange}
            onConnect={onConnect}
            fitView
          >
            <Controls />
            <MiniMap />
            <Background variant={BackgroundVariant.Dots} gap={12} size={1} />
          </ReactFlow>
        ) : (
          <div style={{
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            justifyContent: 'center',
            height: '100%',
            gap: '20px'
          }}>
            <p style={{ color: '#9ca3af', fontSize: '18px', margin: 0 }}>
              Граф квеста появится здесь
            </p>
            <button
              onClick={() => setIsLibraryOpen(true)}
              style={{
                padding: '12px 24px',
                background: '#3b82f6',
                color: 'white',
                border: 'none',
                borderRadius: '8px',
                cursor: 'pointer',
                fontSize: '16px'
              }}
            >
              📚 Загрузить квест из библиотеки
            </button>
          </div>
        )}
      </div>
    </div>
  )
}
