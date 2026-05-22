import Weapon from '../src/js/weapons/Weapon';
import Arm from '../src/js/weapons/Arm';
import Bow from '../src/js/weapons/Bow';
import Sword from '../src/js/weapons/Sword';
import Knife from '../src/js/weapons/Knife';
import Staff from '../src/js/weapons/Staff';
import LongBow from '../src/js/weapons/LongBow';
import Axe from '../src/js/weapons/Axe';
import StormStaff from '../src/js/weapons/StormStaff';

describe('Weapon', () => {
  let weapon;

  beforeEach(() => {
    weapon = new Weapon('TestSword', 50, 100, 2);
  });

  test('creates with correct properties', () => {
    expect(weapon.name).toBe('TestSword');
    expect(weapon.attack).toBe(50);
    expect(weapon.durability).toBe(100);
    expect(weapon.range).toBe(2);
  });

  test('takeDamage reduces durability', () => {
    weapon.takeDamage(30);
    expect(weapon.durability).toBe(70);
  });

  test('durability does not go below 0', () => {
    weapon.takeDamage(200);
    expect(weapon.durability).toBe(0);
  });

  test('isBroken returns false when durability > 0', () => {
    expect(weapon.isBroken()).toBe(false);
  });

  test('isBroken returns true when durability is 0', () => {
    weapon.takeDamage(100);
    expect(weapon.isBroken()).toBe(true);
  });

  test('getDamage returns attack value when not broken', () => {
    expect(weapon.getDamage()).toBe(50);
  });

  test('getDamage returns 0 when broken', () => {
    weapon.takeDamage(100);
    expect(weapon.getDamage()).toBe(0);
  });
});

describe('Arm', () => {
  test('has correct default values', () => {
    const arm = new Arm();
    expect(arm.name).toBe('Arm');
    expect(arm.attack).toBe(10);
    expect(arm.durability).toBe(100);
    expect(arm.range).toBe(1);
  });
});

describe('Bow', () => {
  test('has correct default values', () => {
    const bow = new Bow();
    expect(bow.name).toBe('Bow');
    expect(bow.attack).toBe(30);
    expect(bow.range).toBe(5);
  });
});

describe('Sword', () => {
  test('has correct default values', () => {
    const sword = new Sword();
    expect(sword.name).toBe('Sword');
    expect(sword.attack).toBe(40);
    expect(sword.range).toBe(2);
  });
});

describe('Knife', () => {
  test('has correct default values', () => {
    const knife = new Knife();
    expect(knife.name).toBe('Knife');
    expect(knife.attack).toBe(20);
    expect(knife.range).toBe(1);
  });
});

describe('Staff', () => {
  test('has correct default values', () => {
    const staff = new Staff();
    expect(staff.name).toBe('Staff');
    expect(staff.attack).toBe(25);
    expect(staff.range).toBe(4);
  });
});

describe('LongBow', () => {
  test('has greater range than Bow', () => {
    const longbow = new LongBow();
    const bow = new Bow();
    expect(longbow.range).toBeGreaterThan(bow.range);
    expect(longbow.name).toBe('LongBow');
  });
});

describe('Axe', () => {
  test('has greater attack than Sword', () => {
    const axe = new Axe();
    const sword = new Sword();
    expect(axe.attack).toBeGreaterThan(sword.attack);
    expect(axe.name).toBe('Axe');
  });
});

describe('StormStaff', () => {
  test('has greater attack than Staff', () => {
    const stormStaff = new StormStaff();
    const staff = new Staff();
    expect(stormStaff.attack).toBeGreaterThan(staff.attack);
    expect(stormStaff.name).toBe('StormStaff');
  });
});
