import { useState } from 'react';
import { login } from '../utils/auth';

export default function LoginPage({ onLogin }) {
    const [form, setForm] = useState({ email: '', password: '' });
    const [errors, setErrors] = useState({});
    const [loading, setLoading] = useState(false);
    const [apiErr, setApiErr] = useState('');

    const validate = () => {
        const e = {};
        if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(form.email)) {
            e.email = 'Введите корректный email';
        }
        if (form.password.length < 6) {
            e.password = 'Пароль должен содержать не менее 6 символов';
        }
        return e;
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        const errs = validate();
        if (Object.keys(errs).length) {
            setErrors(errs);
            return;
        }

        setLoading(true);
        setApiErr('');

        try {
            const user = await login(form.email, form.password);
            onLogin(user);
        } catch (err) {
            setApiErr(err.message);
        } finally {
            setLoading(false);
        }
    };

    const handleChange = (field) => (e) => {
        setForm(prev => ({ ...prev, [field]: e.target.value }));
        if (errors[field]) setErrors(prev => ({ ...prev, [field]: '' }));
    };

    return (
        <div className="login-page">
            <form className="login-form" onSubmit={handleSubmit} noValidate>
                <h2>Вход в систему</h2>

                <div className="field">
                    <label>Email</label>
                    <input
                        type="email"
                        value={form.email}
                        onChange={handleChange('email')}
                        placeholder="user@example.com"
                    />
                    {errors.email && <span className="field-error">{errors.email}</span>}
                </div>

                <div className="field">
                    <label>Пароль</label>
                    <input
                        type="password"
                        value={form.password}
                        onChange={handleChange('password')}
                        placeholder="Минимум 6 символов"
                    />
                    {errors.password && <span className="field-error">{errors.password}</span>}
                </div>

                {apiErr && <div className="api-error">{apiErr}</div>}

                <button type="submit" disabled={loading} className="btn-submit">
                    {loading ? 'Входим...' : 'Войти'}
                </button>
            </form>
        </div>
    );
}
