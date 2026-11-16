import React, { useState, useEffect } from 'react'
import { fetchPlayersAndConfig, fetchPlayerInfo, fetchRecommendations, fetchManagersForPlayer } from '../services/api'
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, Cell, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, Radar, Legend } from 'recharts'
import { Award, Cpu, Calendar, User, TrendingUp, Shield, Activity, Sparkles, PieChart } from 'lucide-react'

export default function Dashboard() {
  const [config, setConfig] = useState({ players: [], years: [], models: [], best_model: 'XGBoost' })
  const [selectedPlayer, setSelectedPlayer] = useState('')
  const [selectedModel, setSelectedModel] = useState('XGBoost')
  const [selectedYear, setSelectedYear] = useState('All')
  
  const [playerInfo, setPlayerInfo] = useState(null)
  const [recommendations, setRecommendations] = useState(null)
  const [managers, setManagers] = useState([])
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    fetchPlayersAndConfig().then(data => {
      setConfig(data)
      if (data.players && data.players.length > 0) {
        setSelectedPlayer(data.players[0].Player_ID)
      }
      if (data.best_model) {
        setSelectedModel(data.best_model)
      }
    }).catch(err => console.error("Error loading config:", err))
  }, [])

  useEffect(() => {
    if (!selectedPlayer) return
    setLoading(true)
    const yearParam = selectedYear === 'All' ? null : selectedYear

    Promise.all([
      fetchPlayerInfo(selectedPlayer, yearParam),
      fetchRecommendations(selectedPlayer, selectedModel, yearParam),
      fetchManagersForPlayer(selectedPlayer, selectedModel, yearParam)
    ]).then(([info, recs, mgrs]) => {
      setPlayerInfo(info)
      setRecommendations(recs)
      setManagers(mgrs.recommended_managers || [])
      setLoading(false)
    }).catch(err => {
      console.error("Error loading dashboard data:", err)
      setLoading(false)
    })
  }, [selectedPlayer, selectedModel, selectedYear])

  const chartData = recommendations?.recommendations?.map(r => ({
    fullName: r.name || r.component,
    name: (r.name || r.component).split(' ')[0],
    value: r.value,
    formation: r.formation || 'Standard'
  })) || []

  const radarData = playerInfo?.scores ? Object.entries(playerInfo.scores).map(([subject, val]) => ({
    subject,
    A: val,
    fullMark: 100
  })) : []

  const activePlayerObj = config.players.find(p => p.Player_ID === selectedPlayer)

  return (
    <div className="space-y-6">
      {/* Controls Bar */}
      <div className="bg-gradient-to-r from-zinc-900 via-zinc-900 to-zinc-900/80 border border-zinc-800 rounded-2xl p-6 shadow-2xl grid grid-cols-1 md:grid-cols-3 gap-4">
        {/* Player Selector */}
        <div>
          <label className="block text-xs font-mono uppercase tracking-wider text-emerald-400 mb-2">Select Player</label>
          <div className="relative">
            <User className="absolute left-3 top-3.5 w-4 h-4 text-emerald-500" />
            <select
              value={selectedPlayer}
              onChange={(e) => setSelectedPlayer(e.target.value)}
              className="w-full bg-zinc-950 border border-zinc-800 rounded-xl pl-10 pr-4 py-3 text-sm text-white focus:outline-none focus:border-emerald-500 transition-all shadow-inner"
            >
              {config.players.map(p => (
                <option key={p.Player_ID} value={p.Player_ID}>
                  {p.Player_Name} ({p.Player_ID})
                </option>
              ))}
            </select>
          </div>
        </div>

        {/* Model Selector */}
        <div>
          <label className="block text-xs font-mono uppercase tracking-wider text-emerald-400 mb-2">ML Inference Model</label>
          <div className="relative">
            <Cpu className="absolute left-3 top-3.5 w-4 h-4 text-emerald-500" />
            <select
              value={selectedModel}
              onChange={(e) => setSelectedModel(e.target.value)}
              className="w-full bg-zinc-950 border border-zinc-800 rounded-xl pl-10 pr-4 py-3 text-sm text-white focus:outline-none focus:border-emerald-500 transition-all shadow-inner"
            >
              {config.models.map(m => (
                <option key={m} value={m}>
                  {m} {m === config.best_model ? '★ (Best F1)' : ''}
                </option>
              ))}
            </select>
          </div>
        </div>

        {/* Year Filter */}
        <div>
          <label className="block text-xs font-mono uppercase tracking-wider text-emerald-400 mb-2">Season / Year Filter</label>
          <div className="relative">
            <Calendar className="absolute left-3 top-3.5 w-4 h-4 text-emerald-500" />
            <select
              value={selectedYear}
              onChange={(e) => setSelectedYear(e.target.value)}
              className="w-full bg-zinc-950 border border-zinc-800 rounded-xl pl-10 pr-4 py-3 text-sm text-white focus:outline-none focus:border-emerald-500 transition-all shadow-inner"
            >
              <option value="All">All Years (Aggregated Profile)</option>
              {config.years.map(y => (
                <option key={y} value={y}>{y}</option>
              ))}
            </select>
          </div>
        </div>
      </div>

      {loading ? (
        <div className="py-24 text-center font-mono text-emerald-400 animate-pulse flex flex-col items-center justify-center space-y-3">
          <Sparkles className="w-8 h-8 animate-spin" />
          <span>Running ML tactical simulation & feature vectors...</span>
        </div>
      ) : (
        <>
          {/* Top Row: Player Avatar Card & Best Tactic Card */}
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            {/* Player Photo Card */}
            <div className="bg-zinc-900 border border-zinc-800 rounded-2xl p-6 shadow-xl flex flex-col items-center justify-center text-center relative overflow-hidden group">
              <div className="absolute inset-0 bg-gradient-to-b from-emerald-500/5 to-transparent pointer-events-none" />
              <div className="w-32 h-32 rounded-2xl overflow-hidden border-2 border-emerald-500/40 shadow-xl mb-4 bg-zinc-950 relative">
                <img
                  src={`/static/images/${selectedPlayer}_img.jpg`}
                  alt={playerInfo?.player_name}
                  className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500"
                  onError={(e) => {
                    e.target.onerror = null;
                    e.target.src = "https://images.unsplash.com/photo-1511882150382-421056c89033?w=300&auto=format&fit=crop&q=80";
                  }}
                />
              </div>
              <h2 className="text-xl font-bold text-white mb-1">{playerInfo?.player_name || activePlayerObj?.Player_Name}</h2>
              <span className="text-xs font-mono text-emerald-400 bg-emerald-500/10 border border-emerald-500/20 px-3 py-1 rounded-full">
                ID: {selectedPlayer}
              </span>
            </div>

            {/* Best Tactic Card */}
            <div className="lg:col-span-2 bg-gradient-to-br from-zinc-900 via-zinc-900 to-emerald-950/20 border border-zinc-800 rounded-2xl p-6 shadow-xl flex flex-col justify-between relative overflow-hidden">
              <div className="absolute top-0 right-0 w-64 h-64 bg-emerald-500/5 rounded-full blur-3xl pointer-events-none" />
              <div>
                <div className="flex items-center justify-between mb-4">
                  <span className="inline-flex items-center space-x-2 bg-emerald-500/10 border border-emerald-500/20 px-3.5 py-1.5 rounded-full text-xs font-mono text-emerald-400 shadow-sm">
                    <Award className="w-4 h-4 text-emerald-400" />
                    <span>Top AI Tactical Recommendation</span>
                  </span>
                  <span className="text-xs font-mono text-zinc-400 bg-zinc-950/80 px-2.5 py-1 rounded-lg border border-zinc-800">
                    Model: {selectedModel}
                  </span>
                </div>
                
                <h2 className="text-2xl font-extrabold text-white mb-2 tracking-tight">
                  {recommendations?.best_tactic_data?.name || 'N/A'}
                </h2>
                <p className="text-sm text-zinc-300 mb-6 leading-relaxed">
                  {recommendations?.best_tactic_data?.description || 'Optimal tactical component maximizing output.'}
                </p>
              </div>

              <div className="grid grid-cols-2 gap-4 pt-4 border-t border-zinc-800/80">
                <div>
                  <span className="text-xs text-zinc-400 block font-mono uppercase">Recommended Formation</span>
                  <span className="text-white font-semibold">{recommendations?.best_tactic_data?.formation || '4-3-3 Possession'}</span>
                </div>
                <div>
                  <span className="text-xs text-zinc-400 block font-mono uppercase">Predicted Impact Score</span>
                  <span className="text-emerald-400 font-mono font-bold text-xl">
                    {recommendations?.best_tactic_data?.value?.toFixed(2) || '0.00'}
                  </span>
                </div>
              </div>
            </div>
          </div>

          {/* Visual Charts Row: Radar Chart & Bar Chart */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {/* Radar Chart for Player Abilities */}
            <div className="bg-zinc-900 border border-zinc-800 rounded-2xl p-6 shadow-xl flex flex-col justify-between">
              <div className="flex items-center justify-between mb-4">
                <h3 className="text-sm font-mono uppercase tracking-wider text-emerald-400 flex items-center space-x-2">
                  <Activity className="w-4 h-4 text-emerald-400" />
                  <span>Ability Radar Profile</span>
                </h3>
                <span className="text-xs font-mono text-zinc-400 bg-zinc-950 px-3 py-1 rounded-lg border border-zinc-800">
                  Passing, Shooting, Creativity...
                </span>
              </div>

              <div className="h-80 w-full flex items-center justify-center">
                <ResponsiveContainer width="100%" height="100%">
                  <RadarChart cx="50%" cy="50%" outerRadius="80%" data={radarData}>
                    <PolarGrid stroke="#27272a" />
                    <PolarAngleAxis dataKey="subject" stroke="#a1a1aa" fontSize={12} />
                    <PolarRadiusAxis angle={30} domain={[0, 100]} stroke="#52525b" />
                    <Radar name="Player Abilities" dataKey="A" stroke="#10b981" fill="#10b981" fillOpacity={0.4} />
                  </RadarChart>
                </ResponsiveContainer>
              </div>
            </div>

            {/* Tactical Components Bar Chart */}
            <div className="bg-zinc-900 border border-zinc-800 rounded-2xl p-6 shadow-xl flex flex-col justify-between">
              <div className="flex items-center justify-between mb-4">
                <h3 className="text-sm font-mono uppercase tracking-wider text-emerald-400 flex items-center space-x-2">
                  <TrendingUp className="w-4 h-4 text-emerald-400" />
                  <span>Tactical Component Impact (1 to 7)</span>
                </h3>
                <span className="text-xs font-mono text-zinc-400 bg-zinc-950 px-3 py-1 rounded-lg border border-zinc-800">
                  Simulated Output Scores
                </span>
              </div>

              <div className="h-80 w-full">
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart data={chartData} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
                    <XAxis dataKey="name" stroke="#71717a" fontSize={11} tickLine={false} interval={0} />
                    <YAxis stroke="#71717a" fontSize={12} tickLine={false} />
                    <Tooltip
                      content={({ active, payload }) => {
                        if (active && payload && payload.length) {
                          const data = payload[0].payload;
                          return (
                            <div className="bg-zinc-900 border border-zinc-700 p-3 rounded-xl shadow-2xl text-xs space-y-1">
                              <p className="font-bold text-emerald-400 text-sm">{data.fullName}</p>
                              <p className="text-zinc-300 font-mono">Formation: {data.formation}</p>
                              <p className="text-emerald-300 font-mono font-bold">Impact Score: {data.value.toFixed(2)}</p>
                            </div>
                          );
                        }
                        return null;
                      }}
                    />
                    <Bar dataKey="value" radius={[8, 8, 0, 0]}>
                      {chartData.map((entry, index) => {
                        const isBest = entry.value === Math.max(...chartData.map(d => d.value));
                        return <Cell key={`cell-${index}`} fill={isBest ? '#10b981' : '#3f3f46'} />;
                      })}
                    </Bar>
                  </BarChart>
                </ResponsiveContainer>
              </div>
            </div>
          </div>

          {/* Recommended Managers Grid */}
          <div className="bg-zinc-900 border border-zinc-800 rounded-2xl p-6 shadow-xl">
            <h3 className="text-sm font-mono uppercase tracking-wider text-emerald-400 mb-6 flex items-center space-x-2">
              <Shield className="w-4 h-4 text-emerald-400" />
              <span>Top Compatible Managers</span>
            </h3>

            <div className="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-5 gap-4">
              {managers.map((mgr, idx) => (
                <div key={mgr.manager_id || idx} className="bg-zinc-950 border border-zinc-800 hover:border-emerald-500/50 rounded-xl p-4 flex flex-col justify-between transition-all group">
                  <div>
                    <span className="text-xs font-mono text-emerald-400 block mb-1">Rank #{idx + 1}</span>
                    <h4 className="font-bold text-white mb-1 group-hover:text-emerald-400 transition-colors">{mgr.manager_name}</h4>
                    <span className="text-xs text-zinc-400 block mb-4 font-mono">
                      Formations: {mgr.formations ? mgr.formations.join(', ') : 'N/A'}
                    </span>
                  </div>
                  <div className="pt-3 border-t border-zinc-900 flex justify-between items-center text-xs font-mono">
                    <span className="text-zinc-400">Match Score:</span>
                    <span className="text-emerald-400 font-bold text-sm">{(mgr.score * 100).toFixed(1)}%</span>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </>
      )}
    </div>
  )
}
