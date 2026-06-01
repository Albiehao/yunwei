<template>
  <div class="table-wrap">
    <table class="table" :class="{ 'table--loading': loading }">
      <thead>
        <tr>
          <th v-for="col in columns" :key="col.key" :style="col.width ? { width: col.width } : {}">
            {{ col.label }}
          </th>
        </tr>
      </thead>
      <tbody>
        <tr v-if="loading && data.length === 0">
          <td :colspan="columns.length">
            <div class="table-skeleton">
              <div v-for="i in 4" :key="i" class="sk-row" :style="{ width: `${85 - i * 8}%` }" />
            </div>
          </td>
        </tr>
        <tr v-else-if="data.length === 0">
          <td :colspan="columns.length" class="table-empty">{{ emptyText }}</td>
        </tr>
        <tr v-for="(row, idx) in data" :key="rowKey ? row[rowKey] : idx">
          <td v-for="col in columns" :key="col.key">
            <slot :name="`cell-${col.key}`" :row="row" :value="row[col.key]">
              {{ col.formatter ? col.formatter(row[col.key], row) : row[col.key] }}
            </slot>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup lang="ts">
import type { TableColumn } from './types'
defineProps<{ columns: TableColumn[]; data: Record<string, any>[]; loading?: boolean; rowKey?: string; emptyText?: string }>()
</script>

<style scoped lang="scss">
.table-wrap {
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  overflow: hidden;
}

.table { width: 100%; border-collapse: collapse; font-size: 13px; }

th {
  text-align: left; padding: 12px 16px;
  font-weight: 500; font-size: 12px;
  color: var(--color-text-muted);
  background: var(--color-bg);
  border-bottom: 1px solid var(--color-border);
  white-space: nowrap;
}

td { padding: 12px 16px; border-bottom: 1px solid var(--color-border-light); color: var(--color-text); }
tbody tr:last-child td { border-bottom: none; }
tbody tr:hover { background: var(--color-bg-hover); }

.table-empty { text-align: center; padding: 40px; color: var(--color-text-muted); }

.table-skeleton { padding: 8px 0; display: flex; flex-direction: column; gap: 10px; }
.sk-row {
  height: 12px; border-radius: 4px;
  background: linear-gradient(90deg, var(--color-border-light) 25%, var(--color-border) 50%, var(--color-border-light) 75%);
  background-size: 200% 100%; animation: sk-shimmer 1.2s infinite;
}
@keyframes sk-shimmer { 0% { background-position: 200% 0; } 100% { background-position: -200% 0; } }
</style>
