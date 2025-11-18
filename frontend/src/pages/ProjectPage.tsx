import { useState } from 'react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { useParams, useNavigate } from 'react-router-dom'
import {
  Container,
  Typography,
  Box,
  Button,
  Card,
  CardContent,
  CardActions,
  Grid,
  CircularProgress,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  Alert,
} from '@mui/material'
import { Add as AddIcon } from '@mui/icons-material'
import { dataService } from '../services/data.service'
import { Table } from '../types/domain'

export default function ProjectPage() {
  const { projectId } = useParams<{ projectId: string }>()
  const navigate = useNavigate()
  const queryClient = useQueryClient()
  const projectIdNum = parseInt(projectId || '0')
  const [openDialog, setOpenDialog] = useState(false)
  const [tableName, setTableName] = useState('')
  const [tableDescription, setTableDescription] = useState('')
  const [error, setError] = useState<string | null>(null)

  const { data: tables, isLoading } = useQuery({
    queryKey: ['tables', projectId],
    queryFn: () => dataService.getTablesByProject(projectIdNum),
    enabled: !!projectId,
  })

  const createMutation = useMutation({
    mutationFn: (data: { name: string; description?: string }) =>
      dataService.createTable(projectIdNum, data.name, data.description),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['tables', projectId] })
      setOpenDialog(false)
      setTableName('')
      setTableDescription('')
      setError(null)
    },
    onError: (err: any) => {
      setError(err.response?.data?.detail || 'Failed to create table')
    },
  })

  const handleCreateTable = () => {
    if (!tableName.trim()) {
      setError('Table name is required')
      return
    }
    setError(null)
    createMutation.mutate({
      name: tableName.trim(),
      description: tableDescription.trim() || undefined,
    })
  }

  if (isLoading) {
    return (
      <Container>
        <Box display="flex" justifyContent="center" alignItems="center" minHeight="80vh">
          <CircularProgress />
        </Box>
      </Container>
    )
  }

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      <Box display="flex" justifyContent="space-between" alignItems="center" mb={3}>
        <Typography variant="h4" component="h1">
          Tables
        </Typography>
        <Button
          variant="contained"
          startIcon={<AddIcon />}
          onClick={() => setOpenDialog(true)}
        >
          New Table
        </Button>
      </Box>

      <Dialog open={openDialog} onClose={() => setOpenDialog(false)} maxWidth="sm" fullWidth>
        <DialogTitle>Create New Table</DialogTitle>
        <DialogContent>
          {error && (
            <Alert severity="error" sx={{ mb: 2 }}>
              {error}
            </Alert>
          )}
          <TextField
            autoFocus
            margin="dense"
            label="Table Name"
            fullWidth
            variant="outlined"
            value={tableName}
            onChange={(e) => setTableName(e.target.value)}
            required
            sx={{ mb: 2 }}
          />
          <TextField
            margin="dense"
            label="Description"
            fullWidth
            variant="outlined"
            multiline
            rows={3}
            value={tableDescription}
            onChange={(e) => setTableDescription(e.target.value)}
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setOpenDialog(false)}>Cancel</Button>
          <Button
            onClick={handleCreateTable}
            variant="contained"
            disabled={createMutation.isPending || !tableName.trim()}
          >
            {createMutation.isPending ? 'Creating...' : 'Create'}
          </Button>
        </DialogActions>
      </Dialog>

      <Grid container spacing={3}>
        {tables?.map((table: Table) => (
          <Grid item xs={12} sm={6} md={4} key={table.id}>
            <Card>
              <CardContent>
                <Typography variant="h6" component="h2">
                  {table.name}
                </Typography>
                <Typography variant="body2" color="text.secondary" sx={{ mt: 1 }}>
                  {table.description || 'No description'}
                </Typography>
                <Typography variant="caption" display="block" sx={{ mt: 1 }}>
                  {table.columns.length} columns
                </Typography>
              </CardContent>
              <CardActions>
                <Button
                  size="small"
                  onClick={() => navigate(`/projects/${projectId}/tables/${table.id}`)}
                >
                  Open
                </Button>
              </CardActions>
            </Card>
          </Grid>
        ))}
        {(!tables || tables.length === 0) && (
          <Grid item xs={12}>
            <Typography variant="body1" color="text.secondary" align="center">
              No tables yet. Create your first table!
            </Typography>
          </Grid>
        )}
      </Grid>
    </Container>
  )
}

