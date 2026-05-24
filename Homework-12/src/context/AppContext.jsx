import { createContext, useContext, useState } from 'react'

export const AppContext = createContext(null)

export function AppProvider({ children }) {
  // кэш списка товаров — чтобы не перезапрашивать при возврате на /list
  const [products, setProducts] = useState([])
  const [favorites, setFavorites] = useState([])
  const [theme, setTheme] = useState('light')

  const toggleFavorite = (product) => {
    setFavorites(prev => {
      const already = prev.some(p => p.id === product.id)
      return already
        ? prev.filter(p => p.id !== product.id)
        : [...prev, product]
    })
  }

  const isFavorite = (id) => favorites.some(p => p.id === id)

  const toggleTheme = () => setTheme(prev => prev === 'light' ? 'dark' : 'light')

  return (
    <AppContext.Provider value={{
      products, setProducts,
      favorites, toggleFavorite, isFavorite,
      theme, toggleTheme
    }}>
      {children}
    </AppContext.Provider>
  )
}

export const useApp = () => useContext(AppContext)
