import React, { useState, useEffect } from 'react'
import { fetchInsights, fetchPlayersAndConfig, fetchImpactOverTime } from '../services/api'
import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer } from 'recharts'
import { TrendingUp, Database, Users, Award } from 'lucide-react'

export default function Insights() {
  const [insights, setInsights] = useState(null)
  const [config, setConfig] = useState({ players: [] })
  const [selectedPlayer, setSelectedPlayer] = useState('')
  const [trendData, setTrendData] = useState([])
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    Promise.all([
      fetchInsights(),
      fetchPlayersAndConfig()
    ]).then(([ins, cfg]) => {
      setInsights(ins)
      setConfig(cfg)
      if (cfg.players && cfg.players.length > 0) {
        setSelectedPlayer(cfg.players[0].Player_ID)
      }
    }).catch(err => console.error("Error loading insights:", err))
  }, [])

  useEffect(() => {
    if (!selectedPlayer) return
    setLoading(true)
    fetchImpactOverTime(selectedPlayer).then(data => {
      setTrendData(data.impact_trend || [])
      setLoading(false)
    }).catch(err => {
      console.error("Error loading trend data:", err)
      setLoading(false)
    })
  }, [selectedPlayer])

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="bg-zinc-900 border border-zinc-800 rounded-2xl p-6 shadow-xl">
        <h2 className="text-xl font-bold text-white flex items-center space-x-2">
          <TrendingUp className="w-5 h-5 text-emerald-400" />
          <span>Capstone Analytics & Performance Insights</span>
        </h2>
        <p className="text-sm text-zinc-400 mt-1">Aggregated dataset metrics and longitudinal player impact trajectory.</p>
      </div>

      {/* Summary KPI Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="bg-zinc-900 border border-zinc-800 rounded-2xl p-6 shadow-xl flex items-center space-x-4">
          <div className="bg-emerald-500/10 border border-emerald-500/20 p-3 rounded-xl text-emerald-400">
            <Users className="w-6 h-6" />
          </div>
          <div>
            <span className="text-xs font-mono text-zinc-400 uppercase">Total Players Tracked</span>
            <span className="text-2xl font-bold text-white block">{insights?.total_players || 0}</span>
          </div>
        </div>

        <div className="bg-zinc-900 border border-zinc-800 rounded-2xl p-6 shadow-xl flex items-center space-x-4">
          <div className="bg-emerald-500/10 border border-emerald-500/20 p-3 rounded-xl text-emerald-400">
            <Database className="w-6 h-6" />
          </div>
          <div>
            <span className="text-xs font-mono text-zinc-400 uppercase">Total Modeling Records</span>
            <span className="text-2xl font-bold text-white block">{insights?.total_records || 0}</span>
          </div>
        </div>

        <div className="bg-zinc-900 border border-zinc-800 rounded-2xl p-6 shadow-xl flex items-center space-x-4">
          <div className="bg-emerald-500/10 border border-emerald-500/20 p-3 rounded-xl text-emerald-400">
            <Award className="w-6 h-6" />
          </div>
          <div>
            <span className="text-xs font-mono text-zinc-400 uppercase">Average Impact Score</span>
            <span className="text-2xl font-bold text-emerald-400 block">{insights?.average_impact_score || 0}</span>
          </div>
        </div>
      </div>

      {/* Trend Over Time Section */}
      <div className="bg-zinc-900 border border-zinc-800 rounded-2xl p-6 shadow-xl space-y-6">
        <div className="flex flex-col md:flex-row items-center justify-between gap-4">
          <h3 className="text-sm font-mono uppercase tracking-wider text-zinc-400">
            Longitudinal Impact Score Trend (By Season)
          </h3>
          <div className="w-full md:w-64">
            <select
              value={selectedPlayer}
              onChange={(e) => setSelectedPlayer(e.target.value)}
              className="w-full bg-zinc-950 border border-zinc-800 rounded-xl px-4 py-2 text-sm text-white focus:outline-none focus:border-emerald-500 transition-colors"
            >
              {config.players.map(p => (
                <option key={p.Player_ID} value={p.Player_ID}>
                  {p.Player_Name} ({p.Player_ID})
                </option>
              ))}
            </select>
          </div>
        </div>

        {loading ? (
          <div className="py-20 text-center text-zinc-400 font-mono animate-pulse">
            Loading trajectory data...
          </div>
        ) : (
          <div className="h-72 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={trendData}>
                <XAxis dataKey="year" stroke="#71717a" fontSize={12} tickLine={false} />
                <YAxis stroke="#71717a" fontSize={12} tickLine={false} />
                <Tooltip
                  contentStyle={{ backgroundColor: '#18181b', borderColor: '#27272a', borderRadius: '12px', color: '#fff' }}
                />
                <Line type="monotone" dataKey="impact_score" stroke="#10b981" strokeWidth={3} dot={{ fill: '#10b981', r: 5 }} />
              </LineChart>
            </ResponsiveContainer>
          </div>
        )}
      </div>
    </div>
  )
}
