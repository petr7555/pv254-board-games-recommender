import { FC } from 'react';
import { useLiveQuery } from 'dexie-react-hooks';
import { Alert, Stack, Typography } from '@mui/material';
import { db } from '../db/db';
import GamesCarousel from './GamesCarousel';
import { minRatings } from '../utils/constants';

type Props = {
  title: string;
  url: string;
};

const PersonalizedGamesCarousel: FC<Props> = ({ title, url }) => {
  const dbRatings = useLiveQuery(() => db.ratings.toArray());
  const dbRatingsLoading = dbRatings === undefined;
  const ratings = dbRatings ?? [];

  if (ratings.length < minRatings) {
    return (
      <Stack spacing={2} direction="column" alignItems="center" sx={{ mt: 4 }}>
        <Typography variant="h4">{title}</Typography>
        {dbRatingsLoading && <Alert severity="info">Loading ratings...</Alert>}
        {!dbRatingsLoading && (
          <Alert severity="warning">
            Rate at least {minRatings} games to get personalized recommendations
          </Alert>
        )}
      </Stack>
    );
  }

  return <GamesCarousel title={title} url={url} ratings={ratings} />;
};

export default PersonalizedGamesCarousel;
