import { lazy, Suspense, type ReactNode } from 'react'
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'
import { AuthProvider } from './contexts/AuthContext'
import { useAuth } from './hooks/useAuth'

const Home = lazy(() => import('./pages/Home'))
const Login = lazy(() => import('./pages/Login'))
const Signup = lazy(() => import('./pages/Signup'))
const EntityCheck = lazy(() => import('./pages/EntityCheck'))
const Pricing = lazy(() => import('./pages/Pricing'))
const BookstoreMap = lazy(() => import('./pages/BookstoreMap'))
const ExamBank = lazy(() => import('./pages/ExamBank'))
const DashboardLayout = lazy(() => import('./components/DashboardLayout'))
const Dashboard = lazy(() => import('./pages/Dashboard'))
const Scans = lazy(() => import('./pages/Scans'))
const Report = lazy(() => import('./pages/Report'))
const PDFReportTemplate = lazy(() => import('./pages/PDFReportTemplate'))

function LoadingScreen() {
  return (
    <div className="min-h-screen flex items-center justify-center bg-brand-light dark:bg-brand-navy">
      <div className="w-10 h-10 border-4 border-brand-blue/30 border-t-brand-blue rounded-full animate-spin" />
    </div>
  )
}

// Protected Route Component
function ProtectedRoute({ children }: { children: ReactNode }) {
  const { user, loading } = useAuth()

  if (loading) {
    return <LoadingScreen />
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
        <Suspense fallback={<LoadingScreen />}>
          <Routes>
            {/* Public Routes */}
            <Route path="/" element={<Home />} />
            <Route path="/login" element={<Login />} />
            <Route path="/entity-check" element={<EntityCheck />} />
            <Route path="/signup" element={<Signup />} />
            <Route path="/docs" element={<Home />} /> {/* Placeholder */}
            <Route path="/pricing" element={<Pricing />} />
            <Route path="/bookstores" element={<BookstoreMap />} />
            <Route path="/exam-bank" element={<ExamBank />} />
            <Route path="/playground" element={<Home />} /> {/* Placeholder */}

            {/* PDF Report Template (for PDF generation) */}
            <Route path="/pdf-report/:scanId" element={<PDFReportTemplate />} />

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
        </Suspense>
      </Router>
    </AuthProvider>
  )
}

export default App
