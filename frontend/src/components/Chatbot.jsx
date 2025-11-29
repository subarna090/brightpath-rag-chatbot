import { useState, useEffect, useRef } from 'react'
import axios from 'axios'
import './Chatbot.css'

const API_URL = 'http://localhost:8000'

const Chatbot = () => {
  const [messages, setMessages] = useState([
    {
      id: 1,
      role: 'assistant',
      content: "👋 Hi! I'm your BrightPath HR Assistant. I can help you with questions about:\n\n• Leave policies (annual, sick, maternity, paternity)\n• Remote work arrangements\n• Performance reviews\n• Travel reimbursement\n• Data security\n• And much more!\n\nTry asking me: \"How many annual leave days do I get?\"",
      sources: [],
      citations: []
    }
  ])
  const [input, setInput] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [expandedCitation, setExpandedCitation] = useState(null)
  const messagesEndRef = useRef(null)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  const handleSubmit = async (e) => {
    e.preventDefault()
    if (!input.trim() || isLoading) return

    const userMessage = {
      id: messages.length + 1,
      role: 'user',
      content: input,
      sources: [],
      citations: []
    }
    
    setMessages(prev => [...prev, userMessage])
    setInput('')
    setIsLoading(true)

    try {
      const response = await axios.post(`${API_URL}/chat`, {
        query: input,
        chat_history: messages
          .filter(m => m.role !== 'assistant' || m.citations.length === 0)
          .map(m => ({ role: m.role, content: m.content }))
      })

      const botMessage = {
        id: messages.length + 2,
        role: 'assistant',
        content: response.data.answer,
        sources: response.data.sources,
        citations: response.data.citations
      }
      setMessages(prev => [...prev, botMessage])
    } catch (error) {
      console.error('Chat error:', error)
      const errorMessage = {
        id: messages.length + 2,
        role: 'assistant',
        content: error.response?.data?.detail || "Sorry, I'm having trouble connecting to the server. Please make sure the backend is running.",
        sources: [],
        citations: []
      }
      setMessages(prev => [...prev, errorMessage])
    } finally {
      setIsLoading(false)
    }
  }

  const handleExampleQuery = (query) => {
    setInput(query)
  }

  const exampleQueries = [
    "How many annual leave days do I get?",
    "What's the remote work policy?",
    "How does performance review work?"
  ]

  return (
    <div className="chatbot-container">
      {/* Header */}
      <div className="chatbot-header">
        <div className="header-content">
          <div className="header-icon">
            <div className="icon-bg"></div>
            <span>🤖</span>
          </div>
          <div className="header-text">
            <h2>HR Policy Assistant</h2>
            <p>Powered by BrightPath Analytics</p>
          </div>
        </div>
      </div>

      {/* Messages Area */}
      <div className="messages-container">
        {messages.map((message, index) => (
          <div key={message.id} className={`message-wrapper ${message.role}`}>
            <div className={`message-bubble ${message.role}`}>
              <div className="message-content">
                {message.content}
              </div>
              
              {/* Citations */}
              {message.citations && message.citations.length > 0 && (
                <div className="citations-section">
                  <div className="citations-header">
                    <span className="citations-icon">📚</span>
                    <span>Sources ({message.citations.length})</span>
                  </div>
                  <div className="citations-list">
                    {message.citations.map((citation, idx) => (
                      <div key={idx} className="citation-item">
                        <div 
                          className="citation-preview"
                          onClick={() => setExpandedCitation(expandedCitation === `${message.id}-${idx}` ? null : `${message.id}-${idx}`)}
                        >
                          <div className="citation-source">
                            <strong>📄 {citation.source}</strong>
                          </div>
                          <div className="citation-text">
                            "{citation.content.substring(0, 100)}..."
                          </div>
                        </div>
                        {expandedCitation === `${message.id}-${idx}` && (
                          <div className="citation-expanded">
                            <p>{citation.content}</p>
                            <small>Source: {citation.source}</small>
                          </div>
                        )}
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>
          </div>
        ))}
        
        {isLoading && (
          <div className="message-wrapper assistant">
            <div className="message-bubble assistant">
              <div className="loading-indicator">
                <div className="spinner"></div>
                <span>BrightPath is thinking...</span>
              </div>
            </div>
          </div>
        )}
        
        <div ref={messagesEndRef} />
      </div>

      {/* Input Area */}
      <div className="input-section">
        <form onSubmit={handleSubmit} className="input-form">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Ask about leave policy, performance reviews, remote work..."
            className="input-field"
            disabled={isLoading}
            autoFocus
          />
          <button
            type="submit"
            disabled={!input.trim() || isLoading}
            className="send-button"
            title="Send message"
          >
            {isLoading ? '⏳' : '➤'}
          </button>
        </form>
        
        {messages.length === 1 && (
          <div className="example-queries">
            <p className="example-label">Try asking:</p>
            <div className="example-buttons">
              {exampleQueries.map((query, idx) => (
                <button
                  key={idx}
                  className="example-button"
                  onClick={() => handleExampleQuery(query)}
                >
                  {query}
                </button>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  )
}

export default Chatbot
