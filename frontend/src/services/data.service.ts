import { apiClient } from './api-client'
import { Project, Table, Row, Version } from '../types/domain'

export const dataService = {
  // Projects
  async getProjects(): Promise<Project[]> {
    const response = await apiClient.get<Project[]>('/api/v1/projects')
    return response.data
  },

  async getProject(projectId: number): Promise<Project> {
    const response = await apiClient.get<Project>(`/api/v1/projects/${projectId}`)
    return response.data
  },

  async createProject(name: string, description?: string): Promise<Project> {
    const response = await apiClient.post<Project>('/api/v1/projects', { name, description })
    return response.data
  },

  // Tables
  async getTablesByProject(projectId: number): Promise<Table[]> {
    const response = await apiClient.get<Table[]>(`/api/v1/tables/project/${projectId}`)
    return response.data
  },

  async getTable(tableId: number): Promise<Table> {
    const response = await apiClient.get<Table>(`/api/v1/tables/${tableId}`)
    return response.data
  },

  async createTable(projectId: number, name: string, description?: string): Promise<Table> {
    const response = await apiClient.post<Table>('/api/v1/tables', {
      project_id: projectId,
      name,
      description,
    })
    return response.data
  },

  // Columns
  async getColumnsByTable(tableId: number): Promise<Column[]> {
    const response = await apiClient.get<Column[]>(`/api/v1/tables/${tableId}/columns`)
    return response.data
  },

  async createColumn(
    tableId: number,
    name: string,
    dataType: string,
    isRequired?: boolean,
    defaultValue?: string,
    enumValues?: string[],
    referenceTableId?: number,
    order?: number
  ): Promise<Column> {
    const response = await apiClient.post<Column>(`/api/v1/tables/${tableId}/columns`, {
      name,
      data_type: dataType,
      is_required: isRequired || false,
      default_value: defaultValue,
      enum_values: enumValues,
      reference_table_id: referenceTableId,
      order: order,
    })
    return response.data
  },

  async deleteColumn(columnId: number): Promise<void> {
    await apiClient.delete(`/api/v1/columns/${columnId}`)
  },

  // Rows
  async createRow(tableId: number, cells: Record<string, any>): Promise<Row> {
    const response = await apiClient.post<Row>('/api/v1/data/rows', {
      table_id: tableId,
      cells,
    })
    return response.data
  },

  async updateRow(rowId: number, cells: Record<string, any>): Promise<Row> {
    const response = await apiClient.patch<Row>(`/api/v1/data/rows/${rowId}`, {
      cells,
    })
    return response.data
  },

  async deleteRow(rowId: number): Promise<void> {
    await apiClient.delete(`/api/v1/data/rows/${rowId}`)
  },

  async updateCell(cellId: number, value: any): Promise<void> {
    await apiClient.patch('/api/v1/data/cell', {
      cell_id: cellId,
      value,
    })
  },

  // Data
  async getTableData(tableId: number, skip = 0, limit = 100): Promise<{ table_id: number; rows: Row[] }> {
    const response = await apiClient.get<{ table_id: number; rows: Row[] }>(
      `/api/v1/data/table/${tableId}`,
      { params: { skip, limit } }
    )
    return response.data
  },

  async updateCell(cellId: number, value: any): Promise<void> {
    await apiClient.patch('/api/v1/data/cell', { cell_id: cellId, value })
  },

  // Versions
  async getVersionsByProject(projectId: number, skip = 0, limit = 100): Promise<Version[]> {
    const response = await apiClient.get<Version[]>(`/api/v1/versions/project/${projectId}`, {
      params: { skip, limit },
    })
    return response.data
  },

  async createCommit(
    projectId: number,
    message: string,
    changes: Record<string, any>,
    tableId?: number
  ): Promise<Version> {
    const response = await apiClient.post<Version>('/api/v1/versions/commit', {
      project_id: projectId,
      table_id: tableId,
      message,
      changes,
    })
    return response.data
  },

  async getDiff(versionId: number): Promise<any> {
    const response = await apiClient.get(`/api/v1/versions/${versionId}/diff`)
    return response.data
  },

  async rollback(versionId: number): Promise<void> {
    await apiClient.post(`/api/v1/versions/${versionId}/rollback`)
  },

  // Code Generation
  async generateCode(tableId: number, format: 'unity' | 'unreal' | 'json'): Promise<Blob> {
    const response = await apiClient.get(`/api/v1/code/tables/${tableId}/generate`, {
      params: { format },
      responseType: 'blob',
    })
    return response.data
  },
}

