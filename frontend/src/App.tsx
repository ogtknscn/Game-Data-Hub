import { Routes, Route, Navigate } from 'react-router-dom'
import { useAuthStore } from './store/slices/authSlice'
import LoginPage from './pages/LoginPage'
import RegisterPage from './pages/RegisterPage'
import DashboardPage from './pages/DashboardPage'
import ProjectPage from './pages/ProjectPage'
import TableEditorPage from './pages/TableEditorPage'
import SchemaEditorPage from './pages/SchemaEditorPage'
import VersionControlPage from './pages/VersionControlPage'

function App() {
  const { isAuthenticated } = useAuthStore()

  return (
    <Routes>
      <Route path="/login" element={<LoginPage />} />
      <Route path="/register" element={<RegisterPage />} />
      <Route
        path="/"
        element={isAuthenticated ? <DashboardPage /> : <Navigate to="/login" />}
      />
      <Route
        path="/projects/:projectId"
        element={isAuthenticated ? <ProjectPage /> : <Navigate to="/login" />}
      />
      <Route
        path="/projects/:projectId/tables/:tableId"
        element={isAuthenticated ? <TableEditorPage /> : <Navigate to="/login" />}
      />
      <Route
        path="/projects/:projectId/tables/:tableId/schema"
        element={isAuthenticated ? <SchemaEditorPage /> : <Navigate to="/login" />}
      />
      <Route
        path="/projects/:projectId/versions"
        element={isAuthenticated ? <VersionControlPage /> : <Navigate to="/login" />}
      />
    </Routes>
  )
}

export default App

