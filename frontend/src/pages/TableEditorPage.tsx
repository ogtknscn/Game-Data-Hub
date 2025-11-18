import { useState } from 'react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { useParams, useNavigate } from 'react-router-dom'
import {
  Container,
  Typography,
  Box,
  Paper,
  CircularProgress,
  Table as MuiTable,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Button,
  IconButton,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  Alert,
  Select,
  MenuItem,
  FormControl,
  InputLabel,
  Tabs,
  Tab,
} from '@mui/material'
import { Add as AddIcon, Delete as DeleteIcon, Edit as EditIcon, Save as SaveIcon, Code as CodeIcon } from '@mui/icons-material'
import { dataService } from '../services/data.service'
import { Table, Row } from '../types/domain'
import EditableCell from '../components/table-editor/EditableCell'

export default function TableEditorPage() {
  const { tableId, projectId } = useParams<{ tableId: string; projectId: string }>()
  const navigate = useNavigate()
  const queryClient = useQueryClient()
  const tableIdNum = parseInt(tableId || '0')
  const [newRowDialogOpen, setNewRowDialogOpen] = useState(false)
  const [newRowCells, setNewRowCells] = useState<Record<string, any>>({})
  const [error, setError] = useState<string | null>(null)
  const [commitDialogOpen, setCommitDialogOpen] = useState(false)
  const [commitMessage, setCommitMessage] = useState('')
  const [codeGenDialogOpen, setCodeGenDialogOpen] = useState(false)
  const [selectedFormat, setSelectedFormat] = useState<'unity' | 'unreal' | 'json'>('json')
  const [generatedCode, setGeneratedCode] = useState<string>('')

  const { data: table, isLoading: tableLoading } = useQuery({
    queryKey: ['table', tableId],
    queryFn: () => dataService.getTable(tableIdNum),
    enabled: !!tableId,
  })

  const { data: tableData, isLoading: dataLoading } = useQuery({
    queryKey: ['tableData', tableId],
    queryFn: () => dataService.getTableData(tableIdNum),
    enabled: !!tableId,
  })

  const updateRowMutation = useMutation({
    mutationFn: ({ rowId, cells }: { rowId: number; cells: Record<string, any> }) =>
      dataService.updateRow(rowId, cells),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['tableData', tableId] })
    },
    onError: (err: any) => {
      setError(err.response?.data?.detail || 'Failed to update cell')
    },
  })

  const createRowMutation = useMutation({
    mutationFn: (cells: Record<string, any>) => dataService.createRow(tableIdNum, cells),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['tableData', tableId] })
      setNewRowDialogOpen(false)
      setNewRowCells({})
      setError(null)
    },
    onError: (err: any) => {
      setError(err.response?.data?.detail || 'Failed to create row')
    },
  })

  const deleteRowMutation = useMutation({
    mutationFn: (rowId: number) => dataService.deleteRow(rowId),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['tableData', tableId] })
    },
    onError: (err: any) => {
      setError(err.response?.data?.detail || 'Failed to delete row')
    },
  })

  const createCommitMutation = useMutation({
    mutationFn: ({ message, changes }: { message: string; changes: Record<string, any> }) =>
      dataService.createCommit(parseInt(projectId || '0'), message, changes, tableIdNum),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['versions', projectId] })
      setCommitDialogOpen(false)
      setCommitMessage('')
      setError(null)
    },
    onError: (err: any) => {
      setError(err.response?.data?.detail || 'Failed to create commit')
    },
  })

  const handleCellSave = (rowId: number, columnName: string, value: any) => {
    const cells: Record<string, any> = { [columnName]: value }
    updateRowMutation.mutate({ rowId, cells })
  }

  const handleAddRow = () => {
    if (!table) return
    
    // Initialize cells with default values
    const cells: Record<string, any> = {}
    table.columns.forEach((col) => {
      if (col.default_value) {
        cells[col.name] = col.default_value
      }
    })
    setNewRowCells(cells)
    setNewRowDialogOpen(true)
  }

  const handleCreateRow = () => {
    if (!table) return
    
    // Validate required columns
    for (const col of table.columns) {
      if (col.is_required && !newRowCells[col.name]) {
        setError(`Column "${col.name}" is required`)
        return
      }
    }
    
    setError(null)
    createRowMutation.mutate(newRowCells)
  }

  const handleDeleteRow = (rowId: number) => {
    if (window.confirm('Are you sure you want to delete this row?')) {
      deleteRowMutation.mutate(rowId)
    }
  }

  const handleCommit = () => {
    if (!commitMessage.trim()) {
      setError('Commit message is required')
      return
    }
    
    // For now, create a simple commit with empty changes
    // In a real implementation, we'd track changes
    const changes: Record<string, any> = {}
    
    setError(null)
    createCommitMutation.mutate({ message: commitMessage.trim(), changes })
  }

  // Early returns after all hooks
  if (tableLoading || dataLoading) {
    return (
      <Container>
        <Box display="flex" justifyContent="center" alignItems="center" minHeight="80vh">
          <CircularProgress />
        </Box>
      </Container>
    )
  }

  if (!table) {
    return (
      <Container>
        <Typography variant="h6" color="error">
          Table not found
        </Typography>
      </Container>
    )
  }

  return (
    <Container maxWidth="xl" sx={{ mt: 4, mb: 4 }}>
      <Box display="flex" justifyContent="space-between" alignItems="center" mb={2}>
        <Box>
          <Typography variant="h4" component="h1" gutterBottom>
            {table.name}
          </Typography>
          {table.description && (
            <Typography variant="body1" color="text.secondary">
              {table.description}
            </Typography>
          )}
        </Box>
        <Box display="flex" gap={2}>
          <Button
            variant="outlined"
            onClick={() => navigate(`/projects/${projectId}/tables/${tableId}/schema`)}
            startIcon={<EditIcon />}
          >
            Edit Schema
          </Button>
          <Button
            variant="outlined"
            onClick={() => navigate(`/projects/${projectId}/versions`)}
            startIcon={<EditIcon />}
          >
            Version History
          </Button>
          <Button variant="contained" startIcon={<CodeIcon />} onClick={() => setCodeGenDialogOpen(true)}>
            Generate Code
          </Button>
          <Button variant="contained" startIcon={<SaveIcon />} onClick={() => setCommitDialogOpen(true)}>
            Commit Changes
          </Button>
          <Button variant="contained" startIcon={<AddIcon />} onClick={handleAddRow}>
            Add Row
          </Button>
        </Box>
      </Box>

      {error && (
        <Alert severity="error" sx={{ mb: 2 }} onClose={() => setError(null)}>
          {error}
        </Alert>
      )}

      {table.columns.length === 0 && (
        <Alert severity="info" sx={{ mb: 2 }}>
          No columns defined. Please add columns in the Schema Editor first.
        </Alert>
      )}

      <TableContainer component={Paper} sx={{ mt: 3 }}>
        <MuiTable>
          <TableHead>
            <TableRow>
              {table.columns.map((column) => (
                <TableCell key={column.id}>
                  {column.name}
                  {column.is_required && <span style={{ color: 'red' }}> *</span>}
                </TableCell>
              ))}
              <TableCell width={50}>Actions</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {tableData?.rows.map((row: Row) => (
              <TableRow key={row.id}>
                {table.columns.map((column) => (
                  <EditableCell
                    key={column.id}
                    value={row.cells[column.name]}
                    column={column}
                    rowId={row.id!}
                    onSave={handleCellSave}
                  />
                ))}
                <TableCell>
                  <IconButton
                    size="small"
                    color="error"
                    onClick={() => handleDeleteRow(row.id!)}
                  >
                    <DeleteIcon fontSize="small" />
                  </IconButton>
                </TableCell>
              </TableRow>
            ))}
            {(!tableData?.rows || tableData.rows.length === 0) && (
              <TableRow>
                <TableCell colSpan={table.columns.length + 1} align="center">
                  No data yet. Click "Add Row" to add your first row.
                </TableCell>
              </TableRow>
            )}
          </TableBody>
        </MuiTable>
      </TableContainer>

      <Dialog open={newRowDialogOpen} onClose={() => setNewRowDialogOpen(false)} maxWidth="sm" fullWidth>
        <DialogTitle>Add New Row</DialogTitle>
        <DialogContent>
          {error && (
            <Alert severity="error" sx={{ mb: 2 }}>
              {error}
            </Alert>
          )}
          <Box display="flex" flexDirection="column" gap={2} sx={{ mt: 1 }}>
            {table.columns.map((column) => (
              <TextField
                key={column.id}
                label={column.name}
                value={newRowCells[column.name] ?? ''}
                onChange={(e) =>
                  setNewRowCells({ ...newRowCells, [column.name]: e.target.value })
                }
                required={column.is_required}
                type={column.data_type === 'integer' || column.data_type === 'float' ? 'number' : 'text'}
                helperText={column.default_value ? `Default: ${column.default_value}` : undefined}
                fullWidth
              />
            ))}
          </Box>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setNewRowDialogOpen(false)}>Cancel</Button>
          <Button
            onClick={handleCreateRow}
            variant="contained"
            disabled={createRowMutation.isPending}
          >
            {createRowMutation.isPending ? 'Creating...' : 'Create'}
          </Button>
        </DialogActions>
      </Dialog>

      <Dialog open={commitDialogOpen} onClose={() => setCommitDialogOpen(false)} maxWidth="sm" fullWidth>
        <DialogTitle>Commit Changes</DialogTitle>
        <DialogContent>
          {error && (
            <Alert severity="error" sx={{ mb: 2 }}>
              {error}
            </Alert>
          )}
          <TextField
            autoFocus
            margin="dense"
            label="Commit Message"
            fullWidth
            variant="outlined"
            multiline
            rows={3}
            value={commitMessage}
            onChange={(e) => setCommitMessage(e.target.value)}
            placeholder="Describe the changes you made..."
            required
            sx={{ mt: 2 }}
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setCommitDialogOpen(false)}>Cancel</Button>
          <Button
            onClick={handleCommit}
            variant="contained"
            disabled={createCommitMutation.isPending || !commitMessage.trim()}
          >
            {createCommitMutation.isPending ? 'Committing...' : 'Commit'}
          </Button>
        </DialogActions>
      </Dialog>

      <Dialog open={codeGenDialogOpen} onClose={() => setCodeGenDialogOpen(false)} maxWidth="md" fullWidth>
        <DialogTitle>Generate Code</DialogTitle>
        <DialogContent>
          <FormControl fullWidth sx={{ mt: 2, mb: 2 }}>
            <InputLabel>Code Format</InputLabel>
            <Select
              value={selectedFormat}
              label="Code Format"
              onChange={(e) => setSelectedFormat(e.target.value as 'unity' | 'unreal' | 'json')}
            >
              <MenuItem value="unity">Unity C# ScriptableObject</MenuItem>
              <MenuItem value="unreal">Unreal Engine JSON</MenuItem>
              <MenuItem value="json">JSON Schema</MenuItem>
            </Select>
          </FormControl>
          
          {generatedCode && (
            <Box sx={{ mt: 2 }}>
              <Typography variant="subtitle2" gutterBottom>
                Generated Code:
              </Typography>
              <Paper sx={{ p: 2, bgcolor: 'grey.100', maxHeight: 400, overflow: 'auto' }}>
                <Box component="pre" sx={{ margin: 0, fontSize: '0.875rem' }}>
                  {generatedCode}
                </Box>
              </Paper>
            </Box>
          )}
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setCodeGenDialogOpen(false)}>Close</Button>
          <Button
            variant="contained"
            onClick={async () => {
              try {
                const blob = await dataService.generateCode(tableIdNum, selectedFormat)
                const text = await blob.text()
                setGeneratedCode(text)
                
                // Also offer download
                const url = window.URL.createObjectURL(blob)
                const a = document.createElement('a')
                a.href = url
                a.download = `${table?.name}.${selectedFormat === 'unity' ? 'cs' : 'json'}`
                document.body.appendChild(a)
                a.click()
                window.URL.revokeObjectURL(url)
                document.body.removeChild(a)
              } catch (err: any) {
                setError(err.response?.data?.detail || 'Failed to generate code')
              }
            }}
          >
            Generate & Download
          </Button>
        </DialogActions>
      </Dialog>
    </Container>
  )
}

