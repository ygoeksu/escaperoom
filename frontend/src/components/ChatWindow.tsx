import { useEffect, useRef } from 'react'
import type { ChatMessage } from '../types/game'

interface Props {
  messages: ChatMessage[]
}

export default function ChatWindow({ messages }: Props) {
  const bottomRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])

  return (
    <div className="chat-window">
      {messages.map((msg, i) => (
        <div key={i} className={`chat-msg chat-msg--${msg.from}`}>
          <span className="chat-prefix">{msg.from === 'player' ? '>' : '#'}</span>
          <pre className="chat-text">{msg.text}</pre>
        </div>
      ))}
      <div ref={bottomRef} />
    </div>
  )
}
