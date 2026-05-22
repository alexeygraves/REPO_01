import Sword from './Sword';

export default class Axe extends Sword {
  constructor() {
    super();
    this.name = 'Axe';
    this.attack = 50;
    this.durability = 75;
  }
}
