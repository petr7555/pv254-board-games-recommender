import Dexie, { Table } from 'dexie';
import Game from '../types/game';

export interface Rating {
  gameId: number;
  game: Game;
  value: number;
  updatedAt: Date;
}

export class MySubClassedDexie extends Dexie {
  ratings!: Table<Rating>;

  constructor() {
    super('ratingDb');
    this.version(1).stores({
      ratings: 'gameId, updatedAt',
    });
  }
}

export const db = new MySubClassedDexie();
