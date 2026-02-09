import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import Home from './pages/Home'

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Home />} />
        {/* Placeholder for other routes */}
        <Route path="/docs" element={<Home />} />
        <Route path="/pricing" element={<Home />} />
        <Route path="/playground" element={<Home />} />
      </Routes>
    </Router>
  )
}

export default App
