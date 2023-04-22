import PagedRequest from './PagedRequest';
import GameRatingSimple from './GameRatingSimple';

type PersonalizedRecommendationsRequest = PagedRequest & {
  ratings: GameRatingSimple[];
};

export default PersonalizedRecommendationsRequest;
