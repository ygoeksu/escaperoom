import type { CommandResponse, GameState } from '../types/game'

const BASE = ''

export async function getOptions(): Promise<{ games: string[] }> {
  const res = await fetch(`${BASE}/options`)
  if (!res.ok) throw new Error(`Failed to fetch options: ${res.statusText}`)
  return res.json()
}

export async function startGame(userId: string, roomName: string): Promise<GameState> {
  const res = await fetch(`${BASE}/start/${userId}`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ room_name: roomName }),
  })
  if (!res.ok) throw new Error(`Failed to start game: ${res.statusText}`)
  return res.json()
}

export async function sendCommand(userId: string, input: string): Promise<CommandResponse> {
  const res = await fetch(`${BASE}/command/${userId}`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ user_input: input }),
  })
  if (!res.ok) throw new Error(`Command failed: ${res.statusText}`)
  return res.json()
}
