import Game from './Game';
import GameRatingSimple from './GameRatingSimple';

type GameRating = GameRatingSimple & {
  game: Game;
  updatedAt: Date;
};

export default GameRating;
