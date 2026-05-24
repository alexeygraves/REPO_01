import { useEffect, useState } from 'react'
import { useApp } from '../context/AppContext'
import ProductCard from '../components/ProductCard'

const API = 'https://dummyjson.com/products?limit=20'

export default function List() {
  const { products, setProducts } = useApp()
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  useEffect(() => {
    // список уже в контексте — возврат со страницы деталей не делает повторный запрос
    if (products.length > 0) return

    setLoading(true)
    setError(null)

    fetch(API)
      .then(res => {
        if (!res.ok) throw new Error(`Сервер ответил ${res.status}`)
        return res.json()
      })
      .then(data => setProducts(data.products))
      .catch(err => setError(err.message))
      .finally(() => setLoading(false))
  }, [])

  if (loading) {
    return (
      <div className="page">
        <div className="spinner">
          <div className="spinner__circle"></div>
          <span>Загружаю товары...</span>
        </div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="page">
        <div className="error-box">
          <p>Не удалось загрузить товары</p>
          <p className="error-detail">{error}</p>
          <button onClick={() => window.location.reload()} className="btn-primary">
            Попробовать снова
          </button>
        </div>
      </div>
    )
  }

  return (
    <div className="page">
      <h1 className="page__title">Каталог товаров</h1>
      <div className="grid">
        {products.map(p => <ProductCard key={p.id} product={p} />)}
      </div>
    </div>
  )
}
