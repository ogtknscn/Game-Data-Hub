import { useState } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import {
  Container,
  Typography,
  Box,
  Button,
  Paper,
  TextField,
  Select,
  MenuItem,
  FormControl,
  InputLabel,
  IconButton,
  List,
  ListItem,
  ListItemText,
  ListItemSecondaryAction,
  Checkbox,
  FormControlLabel,
  Alert,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Chip,
} from '@mui/material'
import { Add as AddIcon, Delete as DeleteIcon } from '@mui/icons-material'
import { dataService } from '../services/data.service'
import { Table, Column } from '../types/domain'

export default function SchemaEditorPage() {
  const { tableId, projectId } = useParams<{ tableId: string; projectId: string }>()
  const navigate = useNavigate()
  const queryClient = useQueryClient()
  const tableIdNum = parseInt(tableId || '0')
  const [error, setError] = useState<string | null>(null)
  const [deleteDialogOpen, setDeleteDialogOpen] = useState(false)
  const [columnToDelete, setColumnToDelete] = useState<Column | null>(null)

  const { data: table } = useQuery({
    queryKey: ['table', tableId],
    queryFn: () => dataService.getTable(tableIdNum),
    enabled: !!tableId,
  })

  const { data: columns } = useQuery({
    queryKey: ['columns', tableId],
    queryFn: () => dataService.getColumnsByTable(tableIdNum),
    enabled: !!tableId,
  })

  const [newColumn, setNewColumn] = useState({
    name: '',
    data_type: 'string',
    is_required: false,
    default_value: '',
    enum_values: '',
    reference_table_id: '',
  })

  const createColumnMutation = useMutation({
    mutationFn: (data: {
      name: string
      dataType: string
      isRequired: boolean
      defaultValue?: string
      enumValues?: string[]
      referenceTableId?: number
    }) =>
      dataService.createColumn(
        tableIdNum,
        data.name,
        data.dataType,
        data.isRequired,
        data.defaultValue,
        data.enumValues,
        data.referenceTableId
      ),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['columns', tableId] })
      queryClient.invalidateQueries({ queryKey: ['table', tableId] })
      setNewColumn({
        name: '',
        data_type: 'string',
        is_required: false,
        default_value: '',
        enum_values: '',
        reference_table_id: '',
      })
      setError(null)
    },
    onError: (err: any) => {
      setError(err.response?.data?.detail || 'Failed to create column')
    },
  })

  const deleteColumnMutation = useMutation({
    mutationFn: (columnId: number) => dataService.deleteColumn(columnId),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['columns', tableId] })
      queryClient.invalidateQueries({ queryKey: ['table', tableId] })
      setDeleteDialogOpen(false)
      setColumnToDelete(null)
    },
    onError: (err: any) => {
      setError(err.response?.data?.detail || 'Failed to delete column')
    },
  })

  const handleAddColumn = () => {
    if (!newColumn.name.trim()) {
      setError('Column name is required')
      return
    }

    let enumValues: string[] | undefined
    if (newColumn.data_type === 'enum') {
      enumValues = newColumn.enum_values
        .split(',')
        .map((v) => v.trim())
        .filter((v) => v.length > 0)
      if (enumValues.length === 0) {
        setError('Enum type requires at least one value')
        return
      }
    }

    let referenceTableId: number | undefined
    if (newColumn.data_type === 'reference') {
      if (!newColumn.reference_table_id) {
        setError('Reference type requires a reference table ID')
        return
      }
      referenceTableId = parseInt(newColumn.reference_table_id)
      if (isNaN(referenceTableId)) {
        setError('Invalid reference table ID')
        return
      }
    }

    setError(null)
    createColumnMutation.mutate({
      name: newColumn.name.trim(),
      dataType: newColumn.data_type,
      isRequired: newColumn.is_required,
      defaultValue: newColumn.default_value || undefined,
      enumValues,
      referenceTableId,
    })
  }

  const handleDeleteClick = (column: Column) => {
    setColumnToDelete(column)
    setDeleteDialogOpen(true)
  }

  const handleDeleteConfirm = () => {
    if (columnToDelete) {
      deleteColumnMutation.mutate(columnToDelete.id!)
    }
  }

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      <Box display="flex" justifyContent="space-between" alignItems="center" mb={3}>
        <Typography variant="h4" component="h1">
          Schema Editor: {table?.name}
        </Typography>
        <Button onClick={() => navigate(`/projects/${projectId}/tables/${tableId}`)}>
          Back to Table
        </Button>
      </Box>

      {error && (
        <Alert severity="error" sx={{ mb: 2 }} onClose={() => setError(null)}>
          {error}
        </Alert>
      )}

      <Paper sx={{ p: 3, mt: 3 }}>
        <Typography variant="h6" gutterBottom>
          Columns ({columns?.length || 0})
        </Typography>

        <List>
          {columns?.map((column: Column) => (
            <ListItem key={column.id}>
              <ListItemText
                primary={
                  <Box display="flex" alignItems="center" gap={1}>
                    <Typography variant="body1" fontWeight="medium">
                      {column.name}
                    </Typography>
                    <Chip label={column.data_type} size="small" />
                    {column.is_required && <Chip label="Required" size="small" color="error" />}
                  </Box>
                }
                secondary={
                  <Box>
                    {column.default_value && (
                      <Typography variant="caption" display="block">
                        Default: {column.default_value}
                      </Typography>
                    )}
                    {column.enum_values && column.enum_values.length > 0 && (
                      <Typography variant="caption" display="block">
                        Values: {column.enum_values.join(', ')}
                      </Typography>
                    )}
                    {column.reference_table_id && (
                      <Typography variant="caption" display="block">
                        References table: {column.reference_table_id}
                      </Typography>
                    )}
                  </Box>
                }
              />
              <ListItemSecondaryAction>
                <IconButton
                  edge="end"
                  aria-label="delete"
                  onClick={() => handleDeleteClick(column)}
                  color="error"
                >
                  <DeleteIcon />
                </IconButton>
              </ListItemSecondaryAction>
            </ListItem>
          ))}
          {(!columns || columns.length === 0) && (
            <ListItem>
              <ListItemText primary="No columns yet. Add your first column below." />
            </ListItem>
          )}
        </List>

        <Box sx={{ mt: 3, p: 2, border: '1px dashed', borderColor: 'divider', borderRadius: 1 }}>
          <Typography variant="subtitle1" gutterBottom>
            Add New Column
          </Typography>
          <Box display="flex" flexDirection="column" gap={2}>
            <Box display="flex" gap={2} alignItems="center" flexWrap="wrap">
              <TextField
                label="Column Name"
                value={newColumn.name}
                onChange={(e) => setNewColumn({ ...newColumn, name: e.target.value })}
                size="small"
                required
                sx={{ minWidth: 200 }}
              />
              <FormControl size="small" sx={{ minWidth: 120 }}>
                <InputLabel>Data Type</InputLabel>
                <Select
                  value={newColumn.data_type}
                  label="Data Type"
                  onChange={(e) => setNewColumn({ ...newColumn, data_type: e.target.value })}
                >
                  <MenuItem value="string">String</MenuItem>
                  <MenuItem value="integer">Integer</MenuItem>
                  <MenuItem value="float">Float</MenuItem>
                  <MenuItem value="boolean">Boolean</MenuItem>
                  <MenuItem value="enum">Enum</MenuItem>
                  <MenuItem value="reference">Reference</MenuItem>
                </Select>
              </FormControl>
              <FormControlLabel
                control={
                  <Checkbox
                    checked={newColumn.is_required}
                    onChange={(e) => setNewColumn({ ...newColumn, is_required: e.target.checked })}
                  />
                }
                label="Required"
              />
            </Box>

            {newColumn.data_type === 'enum' && (
              <TextField
                label="Enum Values (comma-separated)"
                value={newColumn.enum_values}
                onChange={(e) => setNewColumn({ ...newColumn, enum_values: e.target.value })}
                size="small"
                placeholder="value1, value2, value3"
                helperText="Enter values separated by commas"
              />
            )}

            {newColumn.data_type === 'reference' && (
              <TextField
                label="Reference Table ID"
                type="number"
                value={newColumn.reference_table_id}
                onChange={(e) => setNewColumn({ ...newColumn, reference_table_id: e.target.value })}
                size="small"
                helperText="ID of the table this column references"
              />
            )}

            <TextField
              label="Default Value (optional)"
              value={newColumn.default_value}
              onChange={(e) => setNewColumn({ ...newColumn, default_value: e.target.value })}
              size="small"
            />

            <Button
              variant="contained"
              startIcon={<AddIcon />}
              onClick={handleAddColumn}
              disabled={createColumnMutation.isPending || !newColumn.name.trim()}
            >
              {createColumnMutation.isPending ? 'Adding...' : 'Add Column'}
            </Button>
          </Box>
        </Box>
      </Paper>

      <Dialog open={deleteDialogOpen} onClose={() => setDeleteDialogOpen(false)}>
        <DialogTitle>Delete Column</DialogTitle>
        <DialogContent>
          <Typography>
            Are you sure you want to delete column "{columnToDelete?.name}"? This action cannot be
            undone and will delete all data in this column.
          </Typography>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setDeleteDialogOpen(false)}>Cancel</Button>
          <Button
            onClick={handleDeleteConfirm}
            color="error"
            variant="contained"
            disabled={deleteColumnMutation.isPending}
          >
            {deleteColumnMutation.isPending ? 'Deleting...' : 'Delete'}
          </Button>
        </DialogActions>
      </Dialog>
    </Container>
  )
}


