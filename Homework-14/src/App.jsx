import { Routes, Route, Navigate } from 'react-router-dom';
import { useState } from 'react';
import { getUser } from './utils/auth';
import Header from './components/Header';
import NetworkStatus from './components/NetworkStatus';
import ProtectedRoute from './components/ProtectedRoute';
import LoginPage from './pages/LoginPage';
import HomePage from './pages/HomePage';
import './App.css';

export default function App() {
    const [user, setUser] = useState(getUser);

    return (
        <>
            <Header user={user} onLogout={() => setUser(null)} />
            <NetworkStatus />
            <Routes>
                <Route
                    path="/login"
                    element={user ? <Navigate to="/" replace /> : <LoginPage onLogin={setUser} />}
                />
                <Route
                    path="/"
                    element={
                        <ProtectedRoute user={user}>
                            <HomePage user={user} />
                        </ProtectedRoute>
                    }
                />
                <Route path="*" element={<Navigate to="/" replace />} />
            </Routes>
        </>
    );
}
