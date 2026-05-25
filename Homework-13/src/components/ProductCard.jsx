import { memo } from 'react'
import { Link } from 'react-router-dom'
import { useApp } from '../context/AppContext'

// memo — не перерисовываем карточку если её пропсы не изменились
const ProductCard = memo(function ProductCard({ product }) {
  const { isFavorite, toggleFavorite, addToCart } = useApp()
  const fav = isFavorite(product.id)

  return (
    <article className="card">
      <img
        src={product.thumbnail}
        alt={product.title}
        className="card__img"
        loading="lazy"
      />
      <div className="card__body">
        <h3 className="card__title">{product.title}</h3>
        <p className="card__desc">
          {product.description.length > 90
            ? product.description.slice(0, 90) + '...'
            : product.description}
        </p>
        <div className="card__meta">
          <span className="card__price">${product.price}</span>
          <span className="card__category">{product.category}</span>
        </div>
        <div className="card__actions">
          <button
            onClick={() => toggleFavorite(product)}
            className={`btn-icon ${fav ? 'btn-icon--active' : ''}`}
            title={fav ? 'Убрать из избранного' : 'В избранное'}
          >
            {fav ? '★' : '☆'}
          </button>
          <button
            onClick={() => addToCart(product)}
            className="btn-icon btn-icon--cart"
            title="В корзину"
          >
            +
          </button>
          <Link to={`/list/${product.id}`} className="card__link">
            Подробнее →
          </Link>
        </div>
      </div>
    </article>
  )
})

export default ProductCard
