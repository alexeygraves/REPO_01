import { lazy, Suspense } from 'react'
import { Routes, Route } from 'react-router-dom'
import { useApp } from './context/AppContext'
import Navbar from './components/Navbar'

// ленивая загрузка страниц — бандл разбивается на чанки по маршрутам
const Home = lazy(() => import('./pages/Home'))
const List = lazy(() => import('./pages/List'))
const Details = lazy(() => import('./pages/Details'))
const About = lazy(() => import('./pages/About'))
const Favourites = lazy(() => import('./pages/Favourites'))
const Cart = lazy(() => import('./pages/Cart'))

function PageFallback() {
  return (
    <div className="page">
      <div className="spinner">
        <div className="spinner__circle"></div>
        <span>Загружаю...</span>
      </div>
    </div>
  )
}

export default function App() {
  const { theme } = useApp()

  return (
    <div className={`app ${theme}`}>
      <Navbar />
      <main className="main-content">
        <Suspense fallback={<PageFallback />}>
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/list" element={<List />} />
            <Route path="/list/:id" element={<Details />} />
            <Route path="/about" element={<About />} />
            <Route path="/favourites" element={<Favourites />} />
            <Route path="/cart" element={<Cart />} />
          </Routes>
        </Suspense>
      </main>
    </div>
  )
}
