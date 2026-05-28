export default function HomePage({ user }) {
    return (
        <main className="home-page">
            <h1>Добро пожаловать, {user?.name}</h1>
            <p>Вы успешно авторизованы. Это защищённая страница.</p>

            <div className="product-grid">
                {/* TODO: подключить реальный каталог товаров */}
                {['Товар 1', 'Товар 2', 'Товар 3'].map(p => (
                    <div key={p} className="product-card">{p}</div>
                ))}
            </div>
        </main>
    );
}
