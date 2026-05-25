import { Link } from 'react-router-dom'
import { useApp } from '../context/AppContext'

export default function Favourites() {
  const { favorites, toggleFavorite, addToCart } = useApp()

  if (favorites.length === 0) {
    return (
      <div className="page">
        <h1 className="page__title">Избранное</h1>
        <div className="empty-state">
          <p>Вы ещё ничего не добавили в избранное</p>
          <Link to="/list" className="btn-primary">Перейти в каталог</Link>
        </div>
      </div>
    )
  }

  return (
    <div className="page">
      <h1 className="page__title">Избранное ({favorites.length})</h1>
      <div className="fav-list">
        {favorites.map(product => (
          <div key={product.id} className="fav-item">
            <img
              src={product.thumbnail}
              alt={product.title}
              className="fav-item__img"
              loading="lazy"
            />
            <div className="fav-item__info">
              <Link to={`/list/${product.id}`} className="fav-item__title">
                {product.title}
              </Link>
              <div className="fav-item__meta">
                <span className="fav-item__price">${product.price}</span>
                <span className="fav-item__category">{product.category}</span>
                <span className="fav-item__stock">На складе: {product.stock} шт.</span>
                {product.rating && (
                  <span className="fav-item__rating">{product.rating} ★</span>
                )}
              </div>
            </div>
            <div className="fav-item__actions">
              <button
                onClick={() => addToCart(product)}
                className="btn-secondary"
              >
                В корзину
              </button>
              <button
                onClick={() => toggleFavorite(product)}
                className="btn-remove"
                title="Убрать из избранного"
              >
                Удалить
              </button>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}
