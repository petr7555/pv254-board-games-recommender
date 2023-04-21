import Dexie, { Table } from 'dexie';
import GameRating from '../types/GameRating';


export class MySubClassedDexie extends Dexie {
  ratings!: Table<GameRating>;

  constructor() {
    super('ratingDb');
    this.version(1).stores({
      ratings: 'gameId, updatedAt',
    });
  }
}

export const db = new MySubClassedDexie();
