import { useState } from 'react'
import Chatbot from './components/Chatbot'
import './index.css'

function App() {
  return (
    <div className="w-full h-screen bg-gradient-to-br from-blue-50 via-purple-50 to-pink-50 flex items-center justify-center p-4">
      <div className="w-full max-w-4xl">
        <div className="text-center mb-8">
          <div className="inline-flex items-center gap-4 mb-6">
            <div className="w-16 h-16 bg-gradient-to-r from-blue-500 to-purple-600 rounded-3xl flex items-center justify-center shadow-lg">
              <span className="text-white font-bold text-4xl">B</span>
            </div>
            <div className="text-left">
              <h1 className="text-4xl md:text-5xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
                BrightPath
              </h1>
              <p className="text-lg text-gray-600 font-medium">HR Assistant</p>
              <p className="text-sm text-gray-500">Ask about policies, leave, benefits & more</p>
            </div>
          </div>
        </div>
        
        <Chatbot />
        
        <div className="text-center mt-6 text-sm text-gray-500">
          <p>Powered by RAG • OpenAI • BrightPath Analytics</p>
        </div>
      </div>
    </div>
  )
}

export default App
