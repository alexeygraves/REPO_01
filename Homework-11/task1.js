// синхронный код идет в call stack напрямую — выполняется сразу
console.log('Синхронный код 1');

// setTimeout попадает в Web API, потом в macrotask queue
// даже с задержкой 0 он выполнится ПОСЛЕ всех microtasks
setTimeout(() => console.log('setTimeout 1'), 0);

// Promise.resolve() кладет коллбек в microtask queue
// microtasks всегда обрабатываются раньше macrotasks — вот почему Promise выводится до setTimeout
Promise.resolve().then(() => console.log('Promise 1'));

// снова синхронный код — выполняется до очистки любых очередей
console.log('Синхронный код 2');

// Итоговый порядок:
// 1. Синхронный код 1  — call stack
// 2. Синхронный код 2  — call stack
// 3. Promise 1         — microtask queue (приоритет выше macrotask)
// 4. setTimeout 1      — macrotask queue (ждет пока microtask queue опустеет)
