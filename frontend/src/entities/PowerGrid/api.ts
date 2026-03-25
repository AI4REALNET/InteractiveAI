import http from '@/plugins/http'
import type { Action } from '@/types/entities'

export function applyRecommendation(data: Action<'PowerGrid'>) {
  // [DISABLED] Simulator API is inactive — returning fake success for demo
  // To restore: uncomment the http.post and remove the Promise.resolve
  // return http.post<{ message: string }>(
  //   import.meta.env.VITE_POWERGRID_SIMU + '/api/v1/recommendations',
  //   data
  // )
  return Promise.resolve({ data: { message: 'ok (simulated)' } })
}
