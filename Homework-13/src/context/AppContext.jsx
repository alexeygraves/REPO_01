import { createContext, useContext, useState, useCallback, useMemo, useEffect } from 'react'

export const AppContext = createContext(null)

const LS_FAV_KEY = 'shop_favourites'

export function AppProvider({ children }) {
  const [products, setProducts] = useState([])
  const [theme, setTheme] = useState('light')

  // инициализируем из localStorage, чтобы избранное не терялось между сессиями
  const [favorites, setFavorites] = useState(() => {
    try {
      const raw = localStorage.getItem(LS_FAV_KEY)
      return raw ? JSON.parse(raw) : []
    } catch {
      return []
    }
  })

  const [cart, setCart] = useState([])

  useEffect(() => {
    localStorage.setItem(LS_FAV_KEY, JSON.stringify(favorites))
  }, [favorites])

  const toggleFavorite = useCallback((product) => {
    setFavorites(prev => {
      const exists = prev.some(p => p.id === product.id)
      return exists ? prev.filter(p => p.id !== product.id) : [...prev, product]
    })
  }, [])

  // useCallback важен здесь — ProductCard принимает эту функцию как пропс,
  // без мемоизации каждый ре-рендер родителя будет перерисовывать все карточки
  const isFavorite = useCallback((id) => {
    return favorites.some(p => p.id === id)
  }, [favorites])

  const addToCart = useCallback((product) => {
    setCart(prev => {
      const item = prev.find(p => p.id === product.id)
      if (item) {
        return prev.map(p => p.id === product.id ? { ...p, qty: p.qty + 1 } : p)
      }
      return [...prev, { ...product, qty: 1 }]
    })
  }, [])

  const removeFromCart = useCallback((id) => {
    setCart(prev => prev.filter(p => p.id !== id))
  }, [])

  const cartTotal = useMemo(() => {
    return cart.reduce((sum, p) => sum + p.price * p.qty, 0).toFixed(2)
  }, [cart])

  const toggleTheme = useCallback(() => {
    setTheme(prev => prev === 'light' ? 'dark' : 'light')
  }, [])

  // мемоизируем весь объект контекста, чтобы не было лишних ре-рендеров
  // у всех потребителей при несвязанных изменениях состояния
  const value = useMemo(() => ({
    products, setProducts,
    favorites, toggleFavorite, isFavorite,
    cart, addToCart, removeFromCart, cartTotal,
    theme, toggleTheme,
  }), [products, favorites, toggleFavorite, isFavorite, cart, addToCart, removeFromCart, cartTotal, theme, toggleTheme])

  return (
    <AppContext.Provider value={value}>
      {children}
    </AppContext.Provider>
  )
}

export const useApp = () => useContext(AppContext)
