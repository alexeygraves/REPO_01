import Arm from '../weapons/Arm';
import Knife from '../weapons/Knife';

export default class Player {
  constructor(name) {
    this.name = name;
    this.weapons = [new Arm(), new Knife()];
  }
}
