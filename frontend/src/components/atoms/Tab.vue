<template>
  <button class="cab-tab" :class="{ active }" :disabled><slot></slot></button>
</template>
<script setup lang="ts">
defineProps<{
  active?: boolean
  disabled?: boolean
}>()
</script>
<style lang="scss">
.cab-tab-container {
  padding: 0 calc(var(--unit) / 2);
  border-bottom: 1px solid var(--color-grey-300);
}
.cab-tab {
  &:disabled {
    color: var(--color-grey-600);
    background: color-mix(in srgb, var(--color-background), #ccc 100%);
  }
  cursor: pointer;
  background: color-mix(in srgb, var(--color-background), #ccc 20%);
  font-family: 'Lexend';
  font-weight: 700;
  border: none;
  box-shadow:
    calc(var(--unit) * 0.25) calc(var(--unit) * 0.25) calc(var(--unit) * 0.5)
      color-mix(in srgb, var(--color-background), #000 20%),
    calc(var(--unit) * -0.25) calc(var(--unit) * -0.25) calc(var(--unit) * 0.5)
      color-mix(in srgb, var(--color-background), #ccc 20%);
  border-radius: var(--radius-small) var(--radius-small) 0 0;
  margin: 0 var(--spacing-1);
  padding: var(--spacing-1) var(--spacing-2);

  &.active {
    position: relative;
    color: var(--color-primary);
    box-shadow:
      inset calc(var(--unit) * 0.5) calc(var(--unit) * 0.5) calc(var(--unit) * 1)
        color-mix(in srgb, var(--color-grey-200), #000 20%),
      inset calc(var(--unit) * -0.5) calc(var(--unit) * -0.5) calc(var(--unit) * 1)
        color-mix(in srgb, var(--color-grey-200), #ccc 20%);
    background: var(--color-grey-200);
  }
}
</style>
