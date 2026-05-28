// mock JWT — base64 payload with exp, no real signature
// TODO: replace with real POST /api/login once backend is ready
const mkToken = (email) => {
    const hdr = btoa(JSON.stringify({ alg: 'none', typ: 'JWT' }));
    const payload = btoa(JSON.stringify({
        email,
        name: email.split('@')[0],
        exp: Date.now() + 60 * 60 * 1000
    }));
    return `${hdr}.${payload}.sig`;
};

export const login = async (email, password) => {
    await new Promise(r => setTimeout(r, 500));

    if (!email || password.length < 6) {
        throw new Error('Неверные данные');
    }

    const token = mkToken(email);
    localStorage.setItem('auth_token', token);
    return getUser();
};

export const logout = () => {
    localStorage.removeItem('auth_token');
};

export const getUser = () => {
    const token = localStorage.getItem('auth_token');
    if (!token) return null;

    try {
        const payload = JSON.parse(atob(token.split('.')[1]));
        if (payload.exp < Date.now()) {
            logout();
            return null;
        }
        return { email: payload.email, name: payload.name };
    } catch {
        logout();
        return null;
    }
};
