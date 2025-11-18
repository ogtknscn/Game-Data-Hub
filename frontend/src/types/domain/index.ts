export interface User {
  id: number
  username: string
  email: string
}

export interface Project {
  id: number
  name: string
  description?: string
  owner_id: number
  created_at: string
  updated_at: string
}

export interface Column {
  id: number
  table_id: number
  name: string
  data_type: string
  is_required: boolean
  default_value?: string
  enum_values?: string[]
  reference_table_id?: number
  order: number
}

export interface Table {
  id: number
  project_id: number
  name: string
  description?: string
  columns: Column[]
  created_at: string
  updated_at: string
}

export interface Row {
  id: number
  table_id: number
  cells: Record<string, any>
}

export interface Version {
  id: number
  project_id: number
  table_id?: number
  message: string
  author_id: number
  changes: Record<string, { old_value: any; new_value: any }>
  created_at: string
}

