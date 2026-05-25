import { render, screen } from '@testing-library/react'
import { MemoryRouter } from 'react-router-dom'
import { describe, it, expect, vi } from 'vitest'
import ProductCard from '../components/ProductCard'

const mockProduct = {
  id: 1,
  title: 'Test Product',
  description: 'A short description for testing purposes only',
  price: 99.99,
  thumbnail: 'https://example.com/img.jpg',
  category: 'electronics',
  stock: 10,
  rating: 4.5,
}

// мокаем контекст — тут нам важно только отрендерить карточку,
// поведение самого контекста тестируем отдельно
vi.mock('../context/AppContext', () => ({
  useApp: () => ({
    isFavorite: vi.fn(() => false),
    toggleFavorite: vi.fn(),
    addToCart: vi.fn(),
  }),
}))

function renderCard(product = mockProduct) {
  return render(
    <MemoryRouter>
      <ProductCard product={product} />
    </MemoryRouter>
  )
}

describe('ProductCard', () => {
  it('renders product title', () => {
    renderCard()
    expect(screen.getByText('Test Product')).toBeInTheDocument()
  })

  it('renders price', () => {
    renderCard()
    expect(screen.getByText('$99.99')).toBeInTheDocument()
  })

  it('renders category', () => {
    renderCard()
    expect(screen.getByText('electronics')).toBeInTheDocument()
  })

  it('has a link to product details', () => {
    renderCard()
    const link = screen.getByRole('link', { name: /подробнее/i })
    expect(link).toHaveAttribute('href', '/list/1')
  })

  it('shows unfilled star when not favourite', () => {
    renderCard()
    expect(screen.getByTitle('В избранное')).toBeInTheDocument()
  })

  it('truncates long descriptions', () => {
    const longDesc = 'A'.repeat(100)
    renderCard({ ...mockProduct, description: longDesc })
    expect(screen.getByText(/A+\.\.\./)).toBeInTheDocument()
  })
})
