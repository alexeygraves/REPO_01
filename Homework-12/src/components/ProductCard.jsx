import { Link } from 'react-router-dom'

export default function ProductCard({ product }) {
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
        <Link to={`/list/${product.id}`} className="card__link">
          Подробнее →
        </Link>
      </div>
    </article>
  )
}
