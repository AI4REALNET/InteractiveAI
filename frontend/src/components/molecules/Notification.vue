<template>
  <Card :orientation class="cab-notification" :color="criticalityToColor(criticality)">
    <template #outer>
      <aside><slot name="outer"></slot></aside>
    </template>
    <header>
      <b><slot name="title"></slot></b>
      <aside><slot name="severity"></slot></aside>
    </header>
    <main><slot></slot></main>
    <footer><slot name="actions"></slot></footer>
  </Card>
</template>
<script setup lang="ts">
import type { Criticality } from '@/types/cards'
import { criticalityToColor } from '@/utils/utils'

import Card from '../atoms/Card.vue'

withDefaults(
  defineProps<{
    orientation?: 'left' | 'right' | 'top' | 'bottom'
    criticality: Criticality
  }>(),
  { orientation: 'left' }
)
</script>
<style lang="scss">
.cab-notification {
  scroll-snap-align: start;

  header {
    color: var(--color-card);
    display: flex;
    justify-content: space-between;
    align-items: center;
    aside {
      display: flex;
      align-items: center;
      font-size: 0.75rem;
    }
  }
  main {
    font-size: 0.875rem;
  }

  footer {
    display: flex;
    gap: var(--spacing-1);
  }
}
</style>
