export interface TableColumn {
  key: string
  label: string
  width?: string
  formatter?: (value: any, row: any) => string
}
