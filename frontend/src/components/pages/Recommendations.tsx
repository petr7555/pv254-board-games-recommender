import React, { FC } from 'react';
import usePageTitle from '../../hooks/usePageTitle';
import GamesCarousel from '../GamesCarousel';
import PersonalizedGamesCarousel from '../PersonalizedGamesCarousel';

const Recommendations: FC = () => {
  usePageTitle('Recommendations');

  return (
    <>
      <PersonalizedGamesCarousel/>
      <GamesCarousel title={'Top-rated'} url={'/recommendations/top-rated'}/>
      <GamesCarousel title={'Most rated'} url={'/recommendations/most-rated'}/>
      <GamesCarousel title={'Random picks'} url={'/recommendations/random'}/>
    </>
  );
};

export default Recommendations;
