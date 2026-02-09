import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import Home from './pages/Home'
import Login from './pages/Login'
import Signup from './pages/Signup'

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/login" element={<Login />} />
        <Route path="/signup" element={<Signup />} />
        {/* Placeholder for other routes */}
        <Route path="/docs" element={<Home />} />
        <Route path="/pricing" element={<Home />} />
        <Route path="/playground" element={<Home />} />
        <Route path="/dashboard" element={<Home />} /> {/* Temporary redirect */}
      </Routes>
    </Router>
  )
}

export default App
