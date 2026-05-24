import { Link } from 'react-router-dom'
import { useApp } from '../context/AppContext'

export default function Home() {
  const { favorites } = useApp()

  return (
    <div className="page home">
      <div className="home__hero">
        <h1 className="home__title">Добро пожаловать в ReactShop</h1>
        <p className="home__sub">
          Учебный проект на React + React Router + Context API
        </p>
        <Link to="/list" className="btn-primary">Перейти в каталог</Link>
      </div>

      {favorites.length > 0 && (
        <section className="home__favs">
          <h2>Избранное ({favorites.length})</h2>
          <ul>
            {favorites.map(p => (
              <li key={p.id}>
                <Link to={`/list/${p.id}`}>{p.title}</Link>
                {' — '}${p.price}
              </li>
            ))}
          </ul>
        </section>
      )}
    </div>
  )
}
