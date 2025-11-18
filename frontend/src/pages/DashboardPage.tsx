import { useState } from 'react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { useNavigate } from 'react-router-dom'
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
import { Project } from '../types/domain'

export default function DashboardPage() {
  const navigate = useNavigate()
  const queryClient = useQueryClient()
  const [openDialog, setOpenDialog] = useState(false)
  const [projectName, setProjectName] = useState('')
  const [projectDescription, setProjectDescription] = useState('')
  const [error, setError] = useState<string | null>(null)

  const { data: projects, isLoading } = useQuery({
    queryKey: ['projects'],
    queryFn: () => dataService.getProjects(),
  })

  const createMutation = useMutation({
    mutationFn: (data: { name: string; description?: string }) =>
      dataService.createProject(data.name, data.description),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['projects'] })
      setOpenDialog(false)
      setProjectName('')
      setProjectDescription('')
      setError(null)
    },
    onError: (err: any) => {
      setError(err.response?.data?.detail || 'Failed to create project')
    },
  })

  const handleCreateProject = () => {
    if (!projectName.trim()) {
      setError('Project name is required')
      return
    }
    setError(null)
    createMutation.mutate({
      name: projectName.trim(),
      description: projectDescription.trim() || undefined,
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
          Projects
        </Typography>
        <Button
          variant="contained"
          startIcon={<AddIcon />}
          onClick={() => setOpenDialog(true)}
        >
          New Project
        </Button>
      </Box>

      <Dialog open={openDialog} onClose={() => setOpenDialog(false)} maxWidth="sm" fullWidth>
        <DialogTitle>Create New Project</DialogTitle>
        <DialogContent>
          {error && (
            <Alert severity="error" sx={{ mb: 2 }}>
              {error}
            </Alert>
          )}
          <TextField
            autoFocus
            margin="dense"
            label="Project Name"
            fullWidth
            variant="outlined"
            value={projectName}
            onChange={(e) => setProjectName(e.target.value)}
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
            value={projectDescription}
            onChange={(e) => setProjectDescription(e.target.value)}
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setOpenDialog(false)}>Cancel</Button>
          <Button
            onClick={handleCreateProject}
            variant="contained"
            disabled={createMutation.isPending || !projectName.trim()}
          >
            {createMutation.isPending ? 'Creating...' : 'Create'}
          </Button>
        </DialogActions>
      </Dialog>

      <Grid container spacing={3}>
        {projects?.map((project: Project) => (
          <Grid item xs={12} sm={6} md={4} key={project.id}>
            <Card>
              <CardContent>
                <Typography variant="h6" component="h2">
                  {project.name}
                </Typography>
                <Typography variant="body2" color="text.secondary" sx={{ mt: 1 }}>
                  {project.description || 'No description'}
                </Typography>
              </CardContent>
              <CardActions>
                <Button size="small" onClick={() => navigate(`/projects/${project.id}`)}>
                  Open
                </Button>
              </CardActions>
            </Card>
          </Grid>
        ))}
        {(!projects || projects.length === 0) && (
          <Grid item xs={12}>
            <Typography variant="body1" color="text.secondary" align="center">
              No projects yet. Create your first project!
            </Typography>
          </Grid>
        )}
      </Grid>
    </Container>
  )
}

