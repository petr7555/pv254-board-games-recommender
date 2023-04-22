import { FC } from 'react';
import usePageTitle from '../../hooks/usePageTitle';
import GamesCarousel from '../GamesCarousel';
import PersonalizedGamesCarousel from '../PersonalizedGamesCarousel';
import {
  mostRatedRecommendationsEndpoint,
  randomRecommendationsEndpoint,
  topRatedRecommendationsEndpoint
} from '../../utils/constants';

const Recommendations: FC = () => {
  usePageTitle('Recommendations');

  return (
    <>
      <PersonalizedGamesCarousel/>
      <GamesCarousel title={'Top-rated'} url={topRatedRecommendationsEndpoint}/>
      <GamesCarousel title={'Most rated'} url={mostRatedRecommendationsEndpoint}/>
      <GamesCarousel title={'Random picks'} url={randomRecommendationsEndpoint}/>
    </>
  );
};

export default Recommendations;
