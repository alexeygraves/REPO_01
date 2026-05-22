import Bow from './Bow';

export default class LongBow extends Bow {
  constructor() {
    super();
    this.name = 'LongBow';
    this.attack = 40;
    this.range = 8;
  }
}
