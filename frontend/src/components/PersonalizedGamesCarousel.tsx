import GamesCarousel from './GamesCarousel';
import { FC } from 'react';
import { useLiveQuery } from 'dexie-react-hooks';
import { db } from '../db/db';
import { Alert, Stack, Typography } from '@mui/material';
import { minRatings, personalizedRecommendationsEndpoint } from '../utils/constants';

const title = 'Personalized';

const PersonalizedGamesCarousel: FC = () => {
  const dbRatings = useLiveQuery(() => db.ratings.toArray());
  const dbRatingsLoading = dbRatings === undefined;
  const ratings = dbRatings ?? [];
  
  if (ratings.length < minRatings) {
    return (
      <Stack spacing={2} direction="column" alignItems="center" sx={{ mt: 4 }}>
        <Typography variant="h4">{title}</Typography>
        {dbRatingsLoading && <Alert severity="info">Loading ratings...</Alert>}
        {!dbRatingsLoading && <Alert severity="warning">Rate at least {minRatings} games to get personalized recommendations</Alert>}
      </Stack>
    );
  }

  return <GamesCarousel title={title} url={personalizedRecommendationsEndpoint} ratings={ratings}/>;
};

export default PersonalizedGamesCarousel;
