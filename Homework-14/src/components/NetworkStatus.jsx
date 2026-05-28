import { useState, useEffect, useRef } from 'react';
import { useNetwork } from '../hooks/useNetwork';

export default function NetworkStatus() {
    const isOnline = useNetwork();
    const [msg, setMsg] = useState(null);
    const mounted = useRef(false);

    useEffect(() => {
        // skip first render — don't show "connected" on page load
        if (!mounted.current) {
            mounted.current = true;
            return;
        }

        if (!isOnline) {
            setMsg({ text: 'Вы в офлайне', cls: 'net-offline' });
        } else {
            setMsg({ text: 'Соединение восстановлено', cls: 'net-online' });
            const t = setTimeout(() => setMsg(null), 3000);
            return () => clearTimeout(t);
        }
    }, [isOnline]);

    if (!msg) return null;

    return (
        <div className={`net-status ${msg.cls}`}>
            {msg.text}
        </div>
    );
}
