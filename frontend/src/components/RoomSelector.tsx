interface Props {
  rooms: string[]
  selected: string
  onChange: (room: string) => void
  onStart: () => void
  loading: boolean
}

export default function RoomSelector({ rooms, selected, onChange, onStart, loading }: Props) {
  return (
    <div className="room-selector">
      <h2>Choose a scenario</h2>
      <ul className="room-list">
        {rooms.map((room) => (
          <li key={room}>
            <button
              className={`room-option${selected === room ? ' room-option--active' : ''}`}
              onClick={() => onChange(room)}
            >
              {room.replace(/_/g, ' ')}
            </button>
          </li>
        ))}
      </ul>
      <button
        className="btn-start"
        onClick={onStart}
        disabled={loading || !selected}
      >
        {loading ? 'Starting…' : 'Start Game'}
      </button>
    </div>
  )
}
