// TODO: поменять на реальный endpoint когда будет свой бэкенд
const API_BASE = 'https://jsonplaceholder.typicode.com';

function fetchData(url) {
    return new Promise((resolve, reject) => {
        // искусственная задержка 2 сек по условию задания
        setTimeout(() => {
            fetch(url)
                .then(res => {
                    if (!res.ok) {
                        reject(new Error(`HTTP ${res.status}: ${url}`));
                        return;
                    }
                    return res.json();
                })
                .then(data => resolve(data))
                .catch(err => reject(err));
        }, 2000);
    });
}

fetchData(`${API_BASE}/users`)
    .then(users => {
        console.log('Список пользователей получен, всего:', users.length);
        // берем id первого и идем за его деталями
        return fetchData(`${API_BASE}/users/${users[0].id}`);
    })
    .then(user => {
        console.log('Первый пользователь:');
        console.log('  Имя:', user.name);
        console.log('  Email:', user.email);
        console.log('  Город:', user.address.city);
    })
    .catch(err => {
        console.error('Не удалось загрузить данные:', err.message);
    });
