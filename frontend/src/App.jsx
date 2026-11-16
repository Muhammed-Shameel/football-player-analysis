import React, { useState } from 'react'
import Navbar from './components/Navbar'
import Dashboard from './pages/Dashboard'
import Managers from './pages/Managers'
import Insights from './pages/Insights'

export default function App() {
  const [activeTab, setActiveTab] = useState('dashboard')

  return (
    <div className="min-h-screen bg-zinc-950 text-zinc-100 flex flex-col">
      <Navbar activeTab={activeTab} setActiveTab={setActiveTab} />
      
      <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {activeTab === 'dashboard' && <Dashboard />}
        {activeTab === 'managers' && <Managers />}
        {activeTab === 'insights' && <Insights />}
      </main>

      <footer className="bg-zinc-900 border-t border-zinc-800 py-6 mt-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center text-xs font-mono text-zinc-500">
          Football Tactical Analytics & ML Capstone Project • Full-Stack Architecture (React + Vite + Python REST API)
        </div>
      </footer>
    </div>
  )
}
