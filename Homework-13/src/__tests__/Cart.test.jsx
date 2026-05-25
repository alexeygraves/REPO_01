import { render, screen, fireEvent } from '@testing-library/react'
import { MemoryRouter } from 'react-router-dom'
import { describe, it, expect, vi } from 'vitest'
import Cart from '../pages/Cart'

const removeFromCart = vi.fn()

const cartItems = [
  {
    id: 1,
    title: 'Cart Item One',
    price: 25.00,
    qty: 2,
    thumbnail: 'https://example.com/1.jpg',
    category: 'sports',
  },
  {
    id: 2,
    title: 'Cart Item Two',
    price: 10.00,
    qty: 1,
    thumbnail: 'https://example.com/2.jpg',
    category: 'toys',
  },
]

vi.mock('../context/AppContext', () => ({
  useApp: vi.fn(),
}))

import { useApp } from '../context/AppContext'

function renderCart(cart = [], cartTotal = '0.00') {
  useApp.mockReturnValue({ cart, removeFromCart, cartTotal })
  return render(
    <MemoryRouter>
      <Cart />
    </MemoryRouter>
  )
}

describe('Cart page', () => {
  it('shows empty state when cart is empty', () => {
    renderCart([], '0.00')
    expect(screen.getByText(/корзина пуста/i)).toBeInTheDocument()
  })

  it('renders all cart items', () => {
    renderCart(cartItems, '60.00')
    expect(screen.getByText('Cart Item One')).toBeInTheDocument()
    expect(screen.getByText('Cart Item Two')).toBeInTheDocument()
  })

  it('shows quantity for each item', () => {
    renderCart(cartItems, '60.00')
    expect(screen.getByText('x2')).toBeInTheDocument()
    expect(screen.getByText('x1')).toBeInTheDocument()
  })

  it('shows cart total', () => {
    renderCart(cartItems, '60.00')
    expect(screen.getByText('$60.00')).toBeInTheDocument()
  })

  it('calls removeFromCart when delete button clicked', () => {
    renderCart(cartItems, '60.00')
    const deleteBtns = screen.getAllByRole('button', { name: /удалить/i })
    fireEvent.click(deleteBtns[0])
    expect(removeFromCart).toHaveBeenCalledWith(1)
  })
})
