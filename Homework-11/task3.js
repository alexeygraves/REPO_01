// FIXME: хардкод базового урла, переделать на env переменную
const API_BASE = 'https://jsonplaceholder.typicode.com';

function delay(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

async function fetchData(url) {
    await delay(2000);
    const res = await fetch(url);
    if (!res.ok) throw new Error(`HTTP ${res.status}: ${url}`);
    return res.json();
}

async function main() {
    try {
        const users = await fetchData(`${API_BASE}/users`);
        console.log('Список пользователей получен, всего:', users.length);

        const user = await fetchData(`${API_BASE}/users/${users[0].id}`);
        console.log('Первый пользователь:');
        console.log('  Имя:', user.name);
        console.log('  Email:', user.email);
        console.log('  Город:', user.address.city);
    } catch (err) {
        console.error('Ошибка загрузки:', err.message);
    }
}

main();
