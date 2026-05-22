export default class Weapon {
  constructor(name, attack, durability, range) {
    this.name = name;
    this.attack = attack;
    this.durability = durability;
    this.range = range;
  }

  takeDamage(amount) {
    this.durability = Math.max(0, this.durability - amount);
  }

  getDamage() {
    if (this.isBroken()) return 0;
    return this.attack;
  }

  isBroken() {
    return this.durability <= 0;
  }
}
