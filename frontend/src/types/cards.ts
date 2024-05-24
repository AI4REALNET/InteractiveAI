import type { Entity, Metadata } from './entities'
import type { UUID } from './formats'

export const SEVERITIES = ['INFORMATION', 'COMPLIANT', 'ACTION', 'ALARM'] as const
export type Severity = (typeof SEVERITIES)[number]
export const CRITICALITIES = ['ND', 'ROUTINE', 'LOW', 'MEDIUM', 'HIGH'] as const
export type Criticality = (typeof CRITICALITIES)[number]

type PublisherType = 'EXTERNAL' | 'ENTITY'

export enum CardOperationType {
  ADD = 'ADD',
  UPDATE = 'UPDATE',
  DELETE = 'DELETE',
  ACK = 'ACK'
}

export type Card<T extends Entity = Entity> = {
  severity: Severity
  summary: {
    parameters: { summary: string }
    key: string
  }
  summaryTranslated: string
  keepChildCards: boolean
  hasBeenAcknowledged?: boolean
  hasBeenRead?: boolean
  processInstanceId: UUID
  process: `${Lowercase<T>}Process`
  publisherType: PublisherType
  endDate: number
  publishDate: number
  processVersion: '1'
  title: { parameters: { title: string }; key: string }
  titleTranslated: string
  uid: string
  publisher: string
  entityRecipients: [T]
  id: `${Card['process']}.${Card['processInstanceId']}`
  state: string
  startDate: number
  data: {
    criticality: Criticality
    metadata: Metadata<T>
    parent_event_id: Card['processInstanceId']
  }
}

export interface CardTree<T extends Entity = Entity> extends Card<T> {
  children: CardTree<T>[]
  read?: boolean
}

export type CardAck = {
  cardUid: string
  entitiesAcks: Entity[]
  type: CardOperationType.ACK
  cardId: string
}

export type CardDelete = {
  entityRecipientsIds: Entity[]
  type: CardOperationType.DELETE
  cardId: string
}

export type CardAdd<T extends Entity = Entity> = {
  entityRecipientsIds: Entity[]
  type: CardOperationType.ADD
  card: Card<T>
}

export type CardUpdate<T extends Entity = Entity> = {
  entityRecipientsIds: Entity[]
  type: CardOperationType.UPDATE
  card: Card<T>
}

export type CardEvent<T extends Entity = Entity> = CardAdd<T> | CardUpdate<T> | CardAck | CardDelete
