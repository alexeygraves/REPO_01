import { render, screen, fireEvent } from '@testing-library/react'
import { MemoryRouter } from 'react-router-dom'
import { describe, it, expect, vi } from 'vitest'
import Favourites from '../pages/Favourites'

const mockProducts = [
  {
    id: 1,
    title: 'Product One',
    price: 19.99,
    thumbnail: 'https://example.com/1.jpg',
    category: 'beauty',
    stock: 5,
    rating: 4.2,
  },
  {
    id: 2,
    title: 'Product Two',
    price: 49.99,
    thumbnail: 'https://example.com/2.jpg',
    category: 'electronics',
    stock: 3,
    rating: 3.8,
  },
]

const toggleFavorite = vi.fn()
const addToCart = vi.fn()

function makeContext(favorites = []) {
  return {
    favorites,
    toggleFavorite,
    addToCart,
  }
}

vi.mock('../context/AppContext', () => ({
  useApp: vi.fn(),
}))

import { useApp } from '../context/AppContext'

function renderPage(favorites = []) {
  useApp.mockReturnValue(makeContext(favorites))
  return render(
    <MemoryRouter>
      <Favourites />
    </MemoryRouter>
  )
}

describe('Favourites page', () => {
  it('shows empty state when no favourites', () => {
    renderPage([])
    expect(screen.getByText(/ничего не добавили/i)).toBeInTheDocument()
    expect(screen.getByRole('link', { name: /каталог/i })).toBeInTheDocument()
  })

  it('renders all favourite products', () => {
    renderPage(mockProducts)
    expect(screen.getByText('Product One')).toBeInTheDocument()
    expect(screen.getByText('Product Two')).toBeInTheDocument()
  })

  it('shows product price and category', () => {
    renderPage(mockProducts)
    expect(screen.getByText('$19.99')).toBeInTheDocument()
    expect(screen.getByText('beauty')).toBeInTheDocument()
  })

  it('calls toggleFavorite when remove button clicked', () => {
    renderPage(mockProducts)
    const removeBtns = screen.getAllByRole('button', { name: /удалить/i })
    fireEvent.click(removeBtns[0])
    expect(toggleFavorite).toHaveBeenCalledWith(mockProducts[0])
  })

  it('calls addToCart when cart button clicked', () => {
    renderPage(mockProducts)
    const cartBtns = screen.getAllByRole('button', { name: /корзину/i })
    fireEvent.click(cartBtns[0])
    expect(addToCart).toHaveBeenCalledWith(mockProducts[0])
  })

  it('shows item count in heading', () => {
    renderPage(mockProducts)
    expect(screen.getByText(/избранное \(2\)/i)).toBeInTheDocument()
  })
})
