import GamesCarousel from './GamesCarousel';
import React, { FC } from 'react';
import { useLiveQuery } from 'dexie-react-hooks';
import { db } from '../db/db';
import Typography from '@mui/material/Typography';
import Stack from '@mui/material/Stack';
import { Alert } from '@mui/material';

const title = 'Personalized';
const minRatings = 3;

const PersonalizedGamesCarousel: FC = () => {
  const ratings = useLiveQuery(() => db.ratings.toArray()) ?? [];

  if (ratings.length < minRatings) {
    return (
      <Stack spacing={2} direction="column" alignItems="center" sx={{ mt: 4 }}>
        <Typography variant="h4">{title}</Typography>
        <Alert severity="warning">Rate at least {minRatings} games to get personalized recommendations</Alert>
      </Stack>
    );
  }

  return <GamesCarousel title={title} url={'/recommendations/personalized'} ratings={ratings}/>;
};

export default PersonalizedGamesCarousel;
