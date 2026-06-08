import { useState, useCallback, useEffect } from 'react'
import { getOptions, startGame, sendCommand } from './api/gameApi'
import type { ChatMessage, GameState } from './types/game'
import ChatWindow from './components/ChatWindow'
import CommandInput from './components/CommandInput'
import CommandReference from './components/CommandReference'
import GameStatus from './components/GameStatus'
import RoomSelector from './components/RoomSelector'

const USER_ID = 'player_' + Math.random().toString(36).slice(2, 8)

export default function App() {
  const [rooms, setRooms] = useState<string[]>([])
  const [selectedRoom, setSelectedRoom] = useState('')
  const [messages, setMessages] = useState<ChatMessage[]>([])
  const [input, setInput] = useState('')
  const [gameState, setGameState] = useState<GameState | null>(null)
  const [loading, setLoading] = useState(false)
  const [started, setStarted] = useState(false)
  const [optionsError, setOptionsError] = useState('')

  useEffect(() => {
    getOptions()
      .then(({ games }) => {
        setRooms(games)
        if (games.length > 0) setSelectedRoom(games[0])
      })
      .catch(() => setOptionsError('Could not reach the backend. Is it running on port 8000?'))
  }, [])

  const appendMsg = (msg: ChatMessage) => setMessages((prev) => [...prev, msg])

  const handleStart = async () => {
    setLoading(true)
    try {
      const state = await startGame(USER_ID, selectedRoom)
      setGameState(state)
      setStarted(true)
      appendMsg({ from: 'game', text: `Started "${selectedRoom.replace(/_/g, ' ')}". Type "look" to see your surroundings.` })
    } catch (err) {
      appendMsg({ from: 'game', text: `Error: ${String(err)}` })
    } finally {
      setLoading(false)
    }
  }

  const handleSubmit = useCallback(async () => {
    const trimmed = input.trim()
    if (!trimmed || loading) return
    setInput('')
    appendMsg({ from: 'player', text: trimmed })
    setLoading(true)
    try {
      const res = await sendCommand(USER_ID, trimmed)
      setGameState(res.state)
      appendMsg({ from: 'game', text: res.message })
      if (res.is_won) {
        appendMsg({ from: 'game', text: '*** You escaped! Congratulations! ***' })
      }
    } catch (err) {
      appendMsg({ from: 'game', text: `Error: ${String(err)}` })
    } finally {
      setLoading(false)
    }
  }, [input, loading])

  return (
    <div className="layout">
      <header className="app-header">
        <h1>Escape Room</h1>
        {started && <GameStatus state={gameState} />}
      </header>

      <div className="main-area">
        <section className="chat-area">
          {!started ? (
            <div className="splash">
              {optionsError ? (
                <p className="splash-error">{optionsError}</p>
              ) : rooms.length === 0 ? (
                <p>Loading scenarios…</p>
              ) : (
                <RoomSelector
                  rooms={rooms}
                  selected={selectedRoom}
                  onChange={setSelectedRoom}
                  onStart={handleStart}
                  loading={loading}
                />
              )}
            </div>
          ) : (
            <>
              <ChatWindow messages={messages} />
              <CommandInput
                value={input}
                onChange={setInput}
                onSubmit={handleSubmit}
                disabled={loading}
              />
            </>
          )}
        </section>

        <CommandReference onInsert={(text) => setInput(text)} />
      </div>
    </div>
  )
}
