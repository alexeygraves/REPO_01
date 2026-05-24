import { Routes, Route } from 'react-router-dom'
import { useApp } from './context/AppContext'
import Navbar from './components/Navbar'
import Home from './pages/Home'
import List from './pages/List'
import Details from './pages/Details'
import About from './pages/About'

export default function App() {
  const { theme } = useApp()

  return (
    <div className={`app ${theme}`}>
      <Navbar />
      <main className="main-content">
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/list" element={<List />} />
          <Route path="/list/:id" element={<Details />} />
          <Route path="/about" element={<About />} />
        </Routes>
      </main>
    </div>
  )
}
