import Archer from './characters/Archer';
import Warrior from './characters/Warrior';
import Mage from './characters/Mage';
import Dwart from './characters/Dwart';
import Crossbowman from './characters/Crossbowman';
import Demourge from './characters/Demourge';

export function play() {
  const team = [
    new Archer('Legolas'),
    new Warrior('Aragorn'),
    new Mage('Gandalf'),
    new Dwart('Gimli'),
    new Crossbowman('Hawkeye'),
    new Demourge('Saruman'),
  ];

  console.log('Team:', team.map((c) => c.name));
}
