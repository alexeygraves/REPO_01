class Weapon {
  constructor(name, attack, durability, range) {
    this.name = name;
    this.attack = attack;
    this.durability = durability;
    this.initialDurability = durability;
    this.range = range;
  }

  takeDamage(damage) {
    this.durability = Math.max(0, this.durability - damage);
  }

  getDamage() {
    if (this.isBroken()) {
      return 0;
    }
    if (this.durability >= this.initialDurability * 0.3) {
      return this.attack;
    }
    return this.attack / 2;
  }

  isBroken() {
    return this.durability === 0;
  }
}

class Arm extends Weapon {
  constructor() {
    super('Рука', 1, Infinity, 1);
  }
}

class Bow extends Weapon {
  constructor() {
    super('Лук', 10, 200, 3);
  }
}

class Sword extends Weapon {
  constructor() {
    super('Меч', 25, 500, 1);
  }
}

class Knife extends Weapon {
  constructor() {
    super('Нож', 5, 300, 1);
  }
}

class Staff extends Weapon {
  constructor() {
    super('Посох', 8, 300, 2);
  }
}

class LongBow extends Bow {
  constructor() {
    super();
    this.name = 'Длинный лук';
    this.attack = 15;
    this.range = 4;
  }
}

class Axe extends Sword {
  constructor() {
    super();
    this.name = 'Секира';
    this.attack = 27;
    this.durability = 800;
    this.initialDurability = 800;
  }
}

class StormStaff extends Staff {
  constructor() {
    super();
    this.name = 'Посох Бури';
    this.attack = 10;
    this.range = 3;
  }
}

class Player {
  constructor(name, position) {
    this.name = name;
    this.position = position;
    this.life = 100;
    this.magic = 20;
    this.speed = 1;
    this.attack = 10;
    this.agility = 5;
    this.luck = 10;
    this.description = 'Игрок';
    this.weapon = new Arm();
    this.weaponChain = [Arm];
    this._weaponIndex = 0;
    this._movingRight = false;
    this._hitCount = 0;
  }

  getLuck() {
    return (Math.random() * 100 + this.luck) / 100;
  }

  getDamage(distance) {
    if (distance > this.weapon.range) {
      return 0;
    }
    const weaponDmg = this.weapon.getDamage();
    return (this.attack + weaponDmg) * this.getLuck() / distance;
  }

  takeDamage(damage) {
    this.life = Math.max(0, this.life - damage);
  }

  isDead() {
    return this.life === 0;
  }

  moveLeft(distance) {
    this.position -= Math.min(distance, this.speed);
    this._movingRight = false;
  }

  moveRight(distance) {
    this.position += Math.min(distance, this.speed);
    this._movingRight = true;
  }

  move(distance) {
    if (distance < 0) {
      this.moveLeft(Math.abs(distance));
    } else {
      this.moveRight(distance);
    }
  }

  isAttackBlocked() {
    return this.getLuck() > (100 - this.luck) / 100;
  }

  dodged() {
    return this.getLuck() > (100 - this.agility - this.speed * 3) / 100;
  }

  takeAttack(damage) {
    if (this.isAttackBlocked()) {
      // attack deflected onto weapon instead of player
      this.weapon.takeDamage(damage);
      return;
    }
    if (this.dodged()) {
      return;
    }
    this.takeDamage(damage);
  }

  checkWeapon() {
    if (this.weapon.isBroken() && this._weaponIndex < this.weaponChain.length - 1) {
      this._weaponIndex++;
      this.weapon = new this.weaponChain[this._weaponIndex]();
    }
  }

  tryAttack(enemy) {
    const distance = Math.abs(this.position - enemy.position);
    const effectiveDist = Math.max(1, distance);

    if (distance > this.weapon.range) {
      return;
    }

    this.weapon.takeDamage(10 * this.getLuck());

    let damage = this.getDamage(effectiveDist);

    // enemy ran into attacker from behind
    if (distance === 0 && enemy._movingRight) {
      damage *= 2;
    }

    enemy.takeAttack(damage);
    this.checkWeapon();
  }

  chooseEnemy(players) {
    const targets = players.filter(p => p !== this && !p.isDead());
    if (targets.length === 0) {
      return null;
    }
    return targets.reduce((weakest, p) => p.life < weakest.life ? p : weakest, targets[0]);
  }

  moveToEnemy(enemy) {
    const diff = this.position - enemy.position;
    if (diff > 0) {
      this.moveLeft(diff);
    } else if (diff < 0) {
      this.moveRight(-diff);
    }
  }

  turn(players) {
    const enemy = this.chooseEnemy(players);
    if (!enemy) {
      return;
    }
    this.moveToEnemy(enemy);
    this.tryAttack(enemy);
  }
}

class Warrior extends Player {
  constructor(name, position) {
    super(name, position);
    this.life = 120;
    this.speed = 2;
    this.description = 'Воин';
    this.weapon = new Sword();
    this.weaponChain = [Sword, Knife, Arm];
    this._maxLife = 120;
  }

  takeDamage(damage) {
    // low HP + luck = damage goes to magic reserve instead of HP
    if (this.life < this._maxLife * 0.5 && this.getLuck() > 0.8) {
      this.magic = Math.max(0, this.magic - damage);
    } else {
      super.takeDamage(damage);
    }
  }

  turn(players) {
    const enemy = this.chooseEnemy(players);
    if (!enemy) {
      return;
    }
    // always close the gap, warrior fights in melee
    this.moveToEnemy(enemy);
    this.tryAttack(enemy);
  }
}

class Archer extends Player {
  constructor(name, position) {
    super(name, position);
    this.life = 80;
    this.magic = 35;
    this.attack = 5;
    this.agility = 10;
    this.description = 'Лучник';
    this.weapon = new Bow();
    this.weaponChain = [Bow, Knife, Arm];
  }

  getDamage(distance) {
    if (distance > this.weapon.range) {
      return 0;
    }
    const weaponDmg = this.weapon.getDamage();
    // more effective at longer range
    return (this.attack + weaponDmg) * this.getLuck() * distance / this.weapon.range;
  }

  turn(players) {
    const enemy = this.chooseEnemy(players);
    if (!enemy) {
      return;
    }
    const dist = Math.abs(this.position - enemy.position);
    if (dist < this.weapon.range) {
      // back away to stay at optimal range
      const diff = this.position - enemy.position;
      if (diff <= 0) {
        this.moveLeft(this.weapon.range - dist);
      } else {
        this.moveRight(this.weapon.range - dist);
      }
    }
    this.tryAttack(enemy);
  }
}

class Mage extends Player {
  constructor(name, position) {
    super(name, position);
    this.life = 70;
    this.magic = 100;
    this.attack = 5;
    this.agility = 8;
    this.description = 'Маг';
    this.weapon = new Staff();
    this.weaponChain = [Staff, Knife, Arm];
    this._maxMagic = 100;
  }

  takeDamage(damage) {
    // magic shield absorbs half damage while mana > 50%
    if (this.magic > this._maxMagic * 0.5) {
      super.takeDamage(damage / 2);
      this.magic = Math.max(0, this.magic - 12);
    } else {
      super.takeDamage(damage);
    }
  }

  turn(players) {
    const enemy = this.chooseEnemy(players);
    if (!enemy) {
      return;
    }
    const dist = Math.abs(this.position - enemy.position);
    if (dist > this.weapon.range) {
      // close in until within staff range
      this.moveToEnemy(enemy);
    } else if (dist < this.weapon.range) {
      // maintain distance, don't let melee fighters get too close
      const diff = this.position - enemy.position;
      if (diff <= 0) {
        this.moveLeft(this.weapon.range - dist);
      } else {
        this.moveRight(this.weapon.range - dist);
      }
    }
    this.tryAttack(enemy);
  }
}

class Dwarf extends Warrior {
  constructor(name, position) {
    super(name, position);
    this.life = 130;
    this.attack = 15;
    this.luck = 20;
    this.description = 'Гном';
    this.weapon = new Axe();
    this.weaponChain = [Axe, Knife, Arm];
    this._maxLife = 130;
  }

  takeDamage(damage) {
    this._hitCount++;
    // TODO: consider making this threshold configurable
    if (this._hitCount % 6 === 0 && this.getLuck() > 0.5) {
      super.takeDamage(damage / 2);
    } else {
      super.takeDamage(damage);
    }
  }
}

class Crossbowman extends Archer {
  constructor(name, position) {
    super(name, position);
    this.life = 85;
    this.attack = 8;
    this.agility = 20;
    this.luck = 15;
    this.description = 'Арбалетчик';
    this.weapon = new LongBow();
    this.weaponChain = [LongBow, Knife, Arm];
  }
}

class Demiurge extends Mage {
  constructor(name, position) {
    super(name, position);
    this.life = 80;
    this.magic = 120;
    this.attack = 6;
    this.luck = 12;
    this.description = 'Демиург';
    this.weapon = new StormStaff();
    this.weaponChain = [StormStaff, Knife, Arm];
    this._maxMagic = 120;
  }

  getDamage(distance) {
    const base = super.getDamage(distance);
    if (this.magic > 0 && this.getLuck() > 0.6) {
      return base * 1.5;
    }
    return base;
  }
}

function play(players) {
  while (true) {
    const alive = players.filter(p => !p.isDead());
    if (alive.length <= 1) {
      return alive[0] || null;
    }
    for (let i = 0; i < alive.length; i++) {
      if (!alive[i].isDead()) {
        alive[i].turn(players);
      }
      const remaining = players.filter(p => !p.isDead());
      if (remaining.length <= 1) {
        return remaining[0] || null;
      }
    }
  }
}
