import type { CommandInfo } from '../types/game'

const COMMANDS: CommandInfo[] = [
  {
    syntax: 'look  (or l)',
    description: 'Describe the current room and its contents.',
    examples: ['look'],
  },
  {
    syntax: 'examine <item>  (or x / inspect)',
    description: 'Inspect an item in the room or your inventory.',
    examples: ['examine beaker', 'x research_journal', 'look at keypad'],
  },
  {
    syntax: 'go <direction>  (or bare direction)',
    description: 'Move to an adjacent room. Directions: north, south, east, west, up, down (n/s/e/w/u/d).',
    examples: ['go north', 'n', 'east'],
  },
  {
    syntax: 'take <item>  (or get / grab / pick)',
    description: 'Pick up an item from the current room.',
    examples: ['take rusty_key', 'get beaker', 'grab golden_scarab'],
  },
  {
    syntax: 'drop <item>',
    description: 'Drop an item from your inventory into the current room.',
    examples: ['drop beaker'],
  },
  {
    syntax: 'inventory  (or i / inv)',
    description: 'List the items you are currently carrying.',
    examples: ['inventory', 'i'],
  },
  {
    syntax: 'use <item>  /  use <item> on <target>',
    description: 'Use an item, optionally on a specific puzzle or object.',
    examples: ['use bronze_key on tomb_door', 'use golden_scarab on altar_lock'],
  },
  {
    syntax: 'solve <puzzle_id> <code>',
    description: 'Enter a numeric or text code for a code-type puzzle.',
    examples: ['solve keypad 4791'],
  },
  {
    syntax: 'help',
    description: 'Show in-game command help.',
    examples: ['help'],
  },
  {
    syntax: 'quit  (or q)',
    description: 'Quit the current game session.',
    examples: ['quit'],
  },
]

interface Props {
  onInsert: (text: string) => void
}

export default function CommandReference({ onInsert }: Props) {
  return (
    <aside className="command-ref">
      <h2>Commands</h2>
      <ul>
        {COMMANDS.map((cmd) => (
          <li key={cmd.syntax} className="cmd-entry">
            <code className="cmd-syntax">{cmd.syntax}</code>
            <p className="cmd-desc">{cmd.description}</p>
            <div className="cmd-examples">
              {cmd.examples.map((ex) => (
                <button
                  key={ex}
                  className="example-chip"
                  title="Click to insert"
                  onClick={() => onInsert(ex)}
                >
                  {ex}
                </button>
              ))}
            </div>
          </li>
        ))}
      </ul>
    </aside>
  )
}
