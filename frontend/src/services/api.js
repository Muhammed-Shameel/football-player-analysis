import axios from 'axios'

const API = axios.create({
  baseURL: import.meta.env.VITE_API_URL || '/api'
})

export const fetchPlayersAndConfig = async () => {
  const response = await API.get('/players')
  return response.data
}

export const fetchManagersList = async () => {
  const response = await API.get('/managers')
  return response.data
}

export const fetchPlayerInfo = async (playerId, year) => {
  const response = await API.get('/player-info', { params: { player_id: playerId, year } })
  return response.data
}

export const fetchRecommendations = async (playerId, model, year) => {
  const response = await API.post('/recommendations', { player_id: playerId, model, year })
  return response.data
}

export const fetchManagersForPlayer = async (playerId, model, year) => {
  const response = await API.post('/managers-for-player', { player_id: playerId, model_name: model, year })
  return response.data
}

export const fetchManagerAnalysis = async (managerId) => {
  const response = await API.get('/manager-analysis', { params: { manager_id: managerId } })
  return response.data
}

export const fetchInsights = async () => {
  const response = await API.get('/insights')
  return response.data
}

export const fetchImpactOverTime = async (playerId) => {
  const response = await API.get('/impact-over-time', { params: { player_id: playerId } })
  return response.data
}

export const fetchSeasonalPerformance = async (playerId) => {
  const response = await API.get('/seasonal-performance', { params: { player_id: playerId } })
  return response.data
}

export const fetchTacticFrequency = async (playerId) => {
  const response = await API.get('/tactic-frequency', { params: { player_id: playerId } })
  return response.data
}
