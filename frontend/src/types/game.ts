export interface GameState {
  current_room_id: string
  inventory: string[]
  solved_puzzles: string[]
  flags: Record<string, string>
  room_items: Record<string, string[]>
  is_won: boolean
  turns: number
}

export interface CommandResponse {
  message: string
  state: GameState
  is_won: boolean
}

export type Scenario = 'labratory'

export interface ChatMessage {
  from: 'player' | 'game'
  text: string
}

export interface CommandInfo {
  syntax: string
  description: string
  examples: string[]
}
