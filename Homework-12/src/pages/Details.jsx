import { useEffect, useState } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { useApp } from '../context/AppContext'

export default function Details() {
  const { id } = useParams()
  const navigate = useNavigate()
  const { isFavorite, toggleFavorite } = useApp()

  const [product, setProduct] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  const fav = product ? isFavorite(product.id) : false

  useEffect(() => {
    setLoading(true)
    setError(null)

    fetch(`https://dummyjson.com/products/${id}`)
      .then(res => {
        if (!res.ok) throw new Error(`Товар не найден (${res.status})`)
        return res.json()
      })
      .then(data => setProduct(data))
      .catch(err => setError(err.message))
      .finally(() => setLoading(false))
  }, [id])

  if (loading) {
    return (
      <div className="page">
        <div className="spinner">
          <div className="spinner__circle"></div>
          <span>Загружаю...</span>
        </div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="page">
        <div className="error-box">
          <p>{error}</p>
          <button onClick={() => navigate(-1)} className="btn-back">← Назад</button>
        </div>
      </div>
    )
  }

  if (!product) return null

  return (
    <div className="page details">
      <button onClick={() => navigate(-1)} className="btn-back">← Назад</button>

      <div className="details__layout">
        <div className="details__gallery">
          <img
            src={product.thumbnail}
            alt={product.title}
            className="details__img"
          />
          <div className="details__thumbs">
            {product.images?.slice(0, 4).map((img, i) => (
              <img key={i} src={img} alt="" className="details__thumb" />
            ))}
          </div>
        </div>

        <div className="details__info">
          <span className="details__category">{product.category}</span>
          <h1 className="details__title">{product.title}</h1>
          <p className="details__desc">{product.description}</p>

          <div className="details__meta">
            <div className="meta-row">
              <span>Цена</span>
              <strong>${product.price}</strong>
            </div>
            <div className="meta-row">
              <span>Рейтинг</span>
              <strong>{product.rating} ★</strong>
            </div>
            <div className="meta-row">
              <span>На складе</span>
              <strong>{product.stock} шт.</strong>
            </div>
            {product.brand && (
              <div className="meta-row">
                <span>Бренд</span>
                <strong>{product.brand}</strong>
              </div>
            )}
          </div>

          <button
            onClick={() => toggleFavorite(product)}
            className={`btn-fav ${fav ? 'btn-fav--active' : ''}`}
          >
            {fav ? '★ Убрать из избранного' : '☆ Добавить в избранное'}
          </button>
        </div>
      </div>
    </div>
  )
}
