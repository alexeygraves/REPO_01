import { Link } from 'react-router-dom'
import { useApp } from '../context/AppContext'

export default function Cart() {
  const { cart, removeFromCart, cartTotal } = useApp()

  if (cart.length === 0) {
    return (
      <div className="page">
        <h1 className="page__title">Корзина</h1>
        <div className="empty-state">
          <p>Корзина пуста</p>
          <Link to="/list" className="btn-primary">Перейти в каталог</Link>
        </div>
      </div>
    )
  }

  return (
    <div className="page">
      <h1 className="page__title">Корзина</h1>
      <div className="cart-layout">
        <div className="cart-list">
          {cart.map(item => (
            <div key={item.id} className="cart-item">
              <img
                src={item.thumbnail}
                alt={item.title}
                className="cart-item__img"
                loading="lazy"
              />
              <div className="cart-item__info">
                <Link to={`/list/${item.id}`} className="cart-item__title">
                  {item.title}
                </Link>
                <span className="cart-item__cat">{item.category}</span>
              </div>
              <div className="cart-item__right">
                <span className="cart-item__qty">x{item.qty}</span>
                <span className="cart-item__price">${(item.price * item.qty).toFixed(2)}</span>
                <button
                  onClick={() => removeFromCart(item.id)}
                  className="btn-remove"
                  title="Убрать из корзины"
                >
                  Удалить
                </button>
              </div>
            </div>
          ))}
        </div>

        <div className="cart-summary">
          <h2 className="cart-summary__title">Итого</h2>
          <div className="cart-summary__row">
            <span>Товаров</span>
            <span>{cart.reduce((sum, p) => sum + p.qty, 0)} шт.</span>
          </div>
          <div className="cart-summary__row cart-summary__total">
            <span>Сумма</span>
            <strong>${cartTotal}</strong>
          </div>
          {/* TODO: добавить форму оформления заказа */}
          <button className="btn-primary cart-summary__btn">
            Оформить заказ
          </button>
        </div>
      </div>
    </div>
  )
}
