import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'
import Home from './pages/Home'
import Login from './pages/Login'
import Signup from './pages/Signup'
import DashboardLayout from './components/DashboardLayout'
import Dashboard from './pages/Dashboard'
import Scans from './pages/Scans'
import Report from './pages/Report'
import { AuthProvider, useAuth } from './contexts/AuthContext'

// Protected Route Component
function ProtectedRoute({ children }: { children: React.ReactNode }) {
  const { user, loading } = useAuth()
  
  if (loading) {
    return <div className="min-h-screen flex items-center justify-center bg-brand-light dark:bg-brand-navy">
      <div className="w-10 h-10 border-4 border-brand-blue/30 border-t-brand-blue rounded-full animate-spin" />
    </div>
  }
  
  if (!user) {
    return <Navigate to="/login" replace />
  }
  return <>{children}</>
}

// Simple Placeholder for other dashboard pages
const Placeholder = ({ title }: { title: string }) => (
  <div className="py-20 text-center">
    <h1 className="text-3xl font-bold text-brand-navy dark:text-brand-light mb-4">{title}</h1>
    <p className="text-brand-slate dark:text-brand-light/60">This feature is coming soon in the next beta update.</p>
  </div>
)

function App() {
  return (
    <AuthProvider>
      <Router>
        <Routes>
          {/* Public Routes */}
          <Route path="/" element={<Home />} />
          <Route path="/login" element={<Login />} />
          <Route path="/signup" element={<Signup />} />
          <Route path="/docs" element={<Home />} /> {/* Placeholder */}
          <Route path="/pricing" element={<Home />} /> {/* Placeholder */}
          <Route path="/playground" element={<Home />} /> {/* Placeholder */}

          {/* Protected Dashboard Routes */}
          <Route 
            path="/dashboard" 
            element={
              <ProtectedRoute>
                <DashboardLayout />
              </ProtectedRoute>
            }
          >
            <Route index element={<Dashboard />} />
            <Route path="scans" element={<Scans />} />
            <Route path="reports" element={<Placeholder title="Reports" />} />
            <Route path="reports/:jobId" element={<Report />} />
            <Route path="settings" element={<Placeholder title="Settings" />} />
          </Route>

          {/* Fallback */}
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </Router>
    </AuthProvider>
  )
}

export default App
