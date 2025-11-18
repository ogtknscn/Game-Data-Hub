import { useParams } from 'react-router-dom'
import { useQuery } from '@tanstack/react-query'
import {
  Container,
  Typography,
  Box,
  Paper,
  List,
  ListItem,
  ListItemText,
  Button,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  CircularProgress,
  Chip,
} from '@mui/material'
import { History as HistoryIcon } from '@mui/icons-material'
import { dataService } from '../services/data.service'
import { Version } from '../types/domain'
import { useState } from 'react'

export default function VersionControlPage() {
  const { projectId, tableId } = useParams<{ projectId: string; tableId?: string }>()
  const projectIdNum = parseInt(projectId || '0')
  const [selectedVersion, setSelectedVersion] = useState<Version | null>(null)
  const [diffDialogOpen, setDiffDialogOpen] = useState(false)
  const [diffData, setDiffData] = useState<any>(null)

  const { data: versions, isLoading } = useQuery({
    queryKey: ['versions', projectId, tableId],
    queryFn: () => dataService.getVersionsByProject(projectIdNum),
    enabled: !!projectId,
  })

  const handleViewDiff = async (version: Version) => {
    try {
      const diff = await dataService.getDiff(version.id)
      setDiffData(diff)
      setSelectedVersion(version)
      setDiffDialogOpen(true)
    } catch (error) {
      console.error('Failed to load diff:', error)
    }
  }

  const handleRollback = async (versionId: number) => {
    if (window.confirm('Are you sure you want to rollback to this version?')) {
      try {
        await dataService.rollback(versionId)
        alert('Rollback successful')
      } catch (error) {
        alert('Rollback failed')
      }
    }
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
      <Box display="flex" alignItems="center" gap={2} mb={3}>
        <HistoryIcon />
        <Typography variant="h4" component="h1">
          Version History
        </Typography>
      </Box>

      <Paper>
        <List>
          {versions?.map((version: Version) => (
            <ListItem
              key={version.id}
              sx={{
                borderBottom: '1px solid',
                borderColor: 'divider',
              }}
            >
              <ListItemText
                primary={version.message}
                secondary={
                  <>
                    <Typography component="span" variant="body2" color="text.primary">
                      {new Date(version.created_at).toLocaleString()}
                    </Typography>
                    <Box sx={{ mt: 1 }}>
                      <Chip
                        label={`${Object.keys(version.changes).length} changes`}
                        size="small"
                        sx={{ mr: 1 }}
                      />
                    </Box>
                  </>
                }
              />
              <Box display="flex" gap={1}>
                <Button size="small" onClick={() => handleViewDiff(version)}>
                  View Diff
                </Button>
                <Button
                  size="small"
                  color="warning"
                  onClick={() => handleRollback(version.id)}
                >
                  Rollback
                </Button>
              </Box>
            </ListItem>
          ))}
          {(!versions || versions.length === 0) && (
            <ListItem>
              <ListItemText primary="No versions yet" />
            </ListItem>
          )}
        </List>
      </Paper>

      <Dialog open={diffDialogOpen} onClose={() => setDiffDialogOpen(false)} maxWidth="md" fullWidth>
        <DialogTitle>
          Diff: {selectedVersion?.message}
        </DialogTitle>
        <DialogContent>
          {diffData && (
            <Box>
              <Typography variant="subtitle2" gutterBottom>
                Changes:
              </Typography>
              <Box component="pre" sx={{ bgcolor: 'grey.100', p: 2, borderRadius: 1, overflow: 'auto' }}>
                {JSON.stringify(diffData.changes, null, 2)}
              </Box>
            </Box>
          )}
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setDiffDialogOpen(false)}>Close</Button>
        </DialogActions>
      </Dialog>
    </Container>
  )
}

