import { NavLink } from 'react-router-dom'
import { useApp } from '../context/AppContext'

export default function Navbar() {
  const { theme, toggleTheme, favorites, cart } = useApp()
  const cartCount = cart.reduce((sum, p) => sum + p.qty, 0)

  return (
    <nav className="navbar">
      <span className="navbar__logo">ReactShop</span>

      <ul className="navbar__links">
        <li>
          <NavLink to="/" end className={({ isActive }) => isActive ? 'nav-link active' : 'nav-link'}>
            Главная
          </NavLink>
        </li>
        <li>
          <NavLink to="/list" className={({ isActive }) => isActive ? 'nav-link active' : 'nav-link'}>
            Каталог
          </NavLink>
        </li>
        <li>
          <NavLink to="/favourites" className={({ isActive }) => isActive ? 'nav-link active' : 'nav-link'}>
            Избранное {favorites.length > 0 && <span className="nav-count">{favorites.length}</span>}
          </NavLink>
        </li>
        <li>
          <NavLink to="/cart" className={({ isActive }) => isActive ? 'nav-link active' : 'nav-link'}>
            Корзина {cartCount > 0 && <span className="nav-count nav-count--cart">{cartCount}</span>}
          </NavLink>
        </li>
        <li>
          <NavLink to="/about" className={({ isActive }) => isActive ? 'nav-link active' : 'nav-link'}>
            О нас
          </NavLink>
        </li>
      </ul>

      <div className="navbar__right">
        <button onClick={toggleTheme} className="theme-toggle" title="Сменить тему">
          {theme === 'light' ? '🌙' : '☀️'}
        </button>
      </div>
    </nav>
  )
}
