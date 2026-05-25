import { Link } from 'react-router-dom'
import { useApp } from '../context/AppContext'

export default function Home() {
  const { favorites, cart } = useApp()
  const cartCount = cart.reduce((sum, p) => sum + p.qty, 0)

  return (
    <div className="page home">
      <div className="home__hero">
        <h1 className="home__title">Добро пожаловать в ReactShop</h1>
        <p className="home__sub">
          Учебный проект на React + Context API + React Router
        </p>
        <div className="home__btns">
          <Link to="/list" className="btn-primary">Перейти в каталог</Link>
          {favorites.length > 0 && (
            <Link to="/favourites" className="btn-secondary">
              Избранное ({favorites.length})
            </Link>
          )}
          {cartCount > 0 && (
            <Link to="/cart" className="btn-secondary">
              Корзина ({cartCount})
            </Link>
          )}
        </div>
      </div>
    </div>
  )
}
