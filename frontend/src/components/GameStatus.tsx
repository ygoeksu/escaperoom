import type { GameState } from '../types/game'

interface Props {
  state: GameState | null
}

export default function GameStatus({ state }: Props) {
  if (!state) return null
  return (
    <div className="game-status">
      <span className="status-item">
        Room: <strong>{state.current_room_id}</strong>
      </span>
      <span className="status-item">
        Turns: <strong>{state.turns}</strong>
      </span>
      <span className="status-item">
        Inventory:{' '}
        <strong>{state.inventory.length > 0 ? state.inventory.join(', ') : 'empty'}</strong>
      </span>
      <span className="status-item">
        Solved: <strong>{state.solved_puzzles.length}</strong>
      </span>
    </div>
  )
}
