import { useRef, useEffect } from 'react'

interface Props {
  value: string
  onChange: (v: string) => void
  onSubmit: () => void
  disabled: boolean
}

export default function CommandInput({ value, onChange, onSubmit, disabled }: Props) {
  const inputRef = useRef<HTMLInputElement>(null)

  useEffect(() => {
    if (!disabled) inputRef.current?.focus()
  }, [disabled])

  return (
    <form
      className="cmd-input-row"
      onSubmit={(e) => {
        e.preventDefault()
        onSubmit()
      }}
    >
      <span className="cmd-prompt">{'>'}</span>
      <input
        ref={inputRef}
        className="cmd-input"
        type="text"
        value={value}
        onChange={(e) => onChange(e.target.value)}
        disabled={disabled}
        placeholder="type a command…"
        autoComplete="off"
        spellCheck={false}
      />
      <button className="cmd-send" type="submit" disabled={disabled || !value.trim()}>
        Send
      </button>
    </form>
  )
}
