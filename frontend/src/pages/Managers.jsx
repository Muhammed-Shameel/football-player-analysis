import React, { useState, useEffect } from 'react'
import { fetchManagersList, fetchManagerAnalysis } from '../services/api'
import { Users, Award, Shield, CheckCircle, Sparkles } from 'lucide-react'

export default function Managers() {
  const [managersList, setManagersList] = useState([])
  const [selectedManager, setSelectedManager] = useState('')
  const [analysis, setAnalysis] = useState(null)
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    fetchManagersList().then(data => {
      if (data.managers && data.managers.length > 0) {
        setManagersList(data.managers)
        setSelectedManager(data.managers[0].manager_id)
      }
    }).catch(err => console.error("Error fetching managers list:", err))
  }, [])

  useEffect(() => {
    if (!selectedManager) return
    setLoading(true)
    fetchManagerAnalysis(selectedManager).then(data => {
      setAnalysis(data)
      setLoading(false)
    }).catch(err => {
      console.error("Error loading manager analysis:", err)
      setLoading(false)
    })
  }, [selectedManager])

  return (
    <div className="space-y-6">
      {/* Manager Selector Header */}
      <div className="bg-gradient-to-r from-zinc-900 via-zinc-900 to-zinc-900/80 border border-zinc-800 rounded-2xl p-6 shadow-xl flex flex-col md:flex-row items-center justify-between gap-4">
        <div>
          <h2 className="text-xl font-bold text-white flex items-center space-x-2">
            <Users className="w-5 h-5 text-emerald-400" />
            <span>Manager Tactical Profile & Analysis</span>
          </h2>
          <p className="text-sm text-zinc-400 mt-1">Explore manager formations, tactical preferences, and compatible players from dataset.</p>
        </div>

        <div className="w-full md:w-80">
          <select
            value={selectedManager}
            onChange={(e) => setSelectedManager(e.target.value)}
            className="w-full bg-zinc-950 border border-zinc-800 rounded-xl px-4 py-3 text-sm text-white focus:outline-none focus:border-emerald-500 transition-colors shadow-inner"
          >
            {managersList.map(m => (
              <option key={m.manager_id} value={m.manager_id}>
                {m.manager_name} ({m.manager_id})
              </option>
            ))}
          </select>
        </div>
      </div>

      {loading ? (
        <div className="py-24 text-center font-mono text-emerald-400 animate-pulse flex flex-col items-center justify-center space-y-3">
          <Sparkles className="w-8 h-8 animate-spin" />
          <span>Loading manager tactical profile...</span>
        </div>
      ) : analysis ? (
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Overview Card */}
          <div className="bg-zinc-900 border border-zinc-800 rounded-2xl p-6 shadow-xl space-y-6">
            <div className="border-b border-zinc-800 pb-4">
              <span className="text-xs font-mono text-emerald-400 uppercase tracking-widest block mb-1">Manager ID: {analysis.manager_id}</span>
              <h3 className="text-2xl font-bold text-white">{analysis.manager_name}</h3>
            </div>

            <div className="space-y-4">
              <div className="bg-zinc-950 border border-zinc-800/80 rounded-xl p-4">
                <span className="text-xs text-zinc-400 block font-mono uppercase mb-1">Preferred Formation</span>
                <span className="text-lg font-bold text-white">{analysis.overview?.preferred_formation}</span>
              </div>
              <div className="bg-zinc-950 border border-zinc-800/80 rounded-xl p-4">
                <span className="text-xs text-zinc-400 block font-mono uppercase mb-1">Tactical System</span>
                <span className="text-sm text-zinc-200 font-medium">{analysis.overview?.tactic_preference}</span>
              </div>
              <div className="bg-zinc-950 border border-zinc-800/80 rounded-xl p-4">
                <span className="text-xs text-zinc-400 block font-mono uppercase mb-1">Estimated Win Rate</span>
                <span className="text-emerald-400 font-mono font-bold text-lg">{analysis.overview?.win_rate}</span>
              </div>
            </div>
          </div>

          {/* Formations & Insights */}
          <div className="lg:col-span-2 space-y-6">
            {/* Formations Breakdown */}
            <div className="bg-zinc-900 border border-zinc-800 rounded-2xl p-6 shadow-xl">
              <h4 className="text-sm font-mono uppercase tracking-wider text-emerald-400 mb-4 flex items-center space-x-2">
                <Shield className="w-4 h-4 text-emerald-400" />
                <span>Formation Usage & Effectiveness</span>
              </h4>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {analysis.formations?.map((f, idx) => (
                  <div key={idx} className="bg-zinc-950 border border-zinc-800 rounded-xl p-4 flex justify-between items-center">
                    <div>
                      <span className="font-bold text-white text-lg block">{f.formation}</span>
                      <span className="text-xs text-zinc-400 font-mono">Usage: {f.usage_percentage}%</span>
                    </div>
                    <div className="text-right font-mono">
                      <span className="text-emerald-400 font-bold block">{f.win_rate}%</span>
                      <span className="text-[10px] text-zinc-400 uppercase">Win Rate</span>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* Strategic Insights */}
            <div className="bg-zinc-900 border border-zinc-800 rounded-2xl p-6 shadow-xl">
              <h4 className="text-sm font-mono uppercase tracking-wider text-emerald-400 mb-4 flex items-center space-x-2">
                <Award className="w-4 h-4 text-emerald-400" />
                <span>Tactical Insights & Philosophy</span>
              </h4>

              <div className="space-y-3">
                {analysis.insights?.map((insight, idx) => (
                  <div key={idx} className="flex items-start space-x-3 bg-zinc-950 border border-zinc-800/80 rounded-xl p-4">
                    <CheckCircle className="w-5 h-5 text-emerald-400 shrink-0 mt-0.5" />
                    <p className="text-sm text-zinc-300 leading-relaxed">{insight}</p>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      ) : null}
    </div>
  )
}
