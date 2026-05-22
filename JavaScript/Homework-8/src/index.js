const characters = [
  {
    name: 'Bowman',
    type: 'Bowman',
    health: 100,
    attack: 25,
    defence: 25,
  },
  {
    name: 'Swordsman',
    type: 'Swordsman',
    health: 100,
    attack: 40,
    defence: 10,
  },
  {
    name: 'Magician',
    type: 'Magician',
    health: 100,
    attack: 10,
    defence: 40,
  },
  {
    name: 'Undead',
    type: 'Undead',
    health: 100,
    attack: 25,
    defence: 25,
  },
  {
    name: 'Zombie',
    type: 'Zombie',
    health: 100,
    attack: 40,
    defence: 10,
  },
  {
    name: 'Daemon',
    type: 'Daemon',
    health: 100,
    attack: 10,
    defence: 40,
  },
];

// only player-controlled characters, enemies start from index 3
const playerChars = characters.filter((char, index) => index < 3);

console.log(playerChars);
