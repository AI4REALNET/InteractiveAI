// Import your theme here
import './PowerGrid/assets/theme.scss'
import './Railway/assets/theme.scss'

// Import your types here
import type { PowerGrid } from './PowerGrid/types'
import type { Railway } from './Railway/types'
// Add your entity and config here
// darkMode: use dark mode
export const ENTITIES_CONFIG = {
  PowerGrid: { darkMode: false },
  Railway: {darkMode: false}
} as const
Object.freeze(ENTITIES_CONFIG)

// Bind your types here
export type EntitiesTypes = {
  PowerGrid: PowerGrid
  Railway: Railway
}
