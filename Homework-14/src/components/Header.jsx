import { useNavigate } from 'react-router-dom';
import { logout } from '../utils/auth';

export default function Header({ user, onLogout }) {
    const nav = useNavigate();

    const handleLogout = () => {
        logout();
        onLogout();
        nav('/login');
    };

    return (
        <header className="header">
            <div className="header-logo">ShopApp</div>
            <div className="header-auth">
                {user ? (
                    <>
                        <span className="user-name">{user.name}</span>
                        <button onClick={handleLogout} className="btn-logout">Выйти</button>
                    </>
                ) : (
                    <button onClick={() => nav('/login')} className="btn-login">Войти</button>
                )}
            </div>
        </header>
    );
}
