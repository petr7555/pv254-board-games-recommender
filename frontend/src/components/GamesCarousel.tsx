import { FC, useCallback, useEffect, useState } from 'react';
import axios from 'axios';
import { Alert, Box, IconButton, Stack, Typography } from '@mui/material';
import GameCard from './GameCard';
import Game from '../types/Game';
import { ArrowBackIosNew as ArrowBack, ArrowForwardIos as ArrowForward } from '@mui/icons-material';
import { useWindowSize } from 'usehooks-ts';
import GamesResponse from '../types/GamesResponse';
import GameRatingSimple from '../types/GameRatingSimple';
import { numberOfGamesPerFetch } from '../utils/constants';

type Props = {
  title?: string;
  url: string;
  searchTerm?: string;
  ratings?: GameRatingSimple[];
}

const GamesCarousel: FC<Props> = ({ title, url, searchTerm, ratings }) => {
  const { width } = useWindowSize();

  const [error, setError] = useState<string>();
  const [loading, setLoading] = useState(true);

  const [games, setGames] = useState<Game[]>([]);
  const [totalNumberOfGames, setTotalNumberOfGames] = useState(0);

  const [carouselOffset, setCarouselOffset] = useState(0);

  useEffect(() => {
    setCarouselOffset(0);
  }, [searchTerm]);

  const fetchGames = useCallback(async (offset: number) => {
    const response = axios.post<GamesResponse>(url, {
      offset,
      limit: numberOfGamesPerFetch,
      ...(searchTerm !== undefined && { searchTerm }),
      ...(ratings && { ratings }),
    });
    const { data } = await response;
    return data;
  }, [ratings, searchTerm, url]);
  
  useEffect(() => {
    setLoading(true);
    fetchGames(0)
      .then((data) => {
        setGames(data.games);
        setTotalNumberOfGames(data.totalNumberOfGames);
      }).catch((err) => {
      setError(err.message);
    }).finally(() => setLoading(false));
  }, [fetchGames]);

  const breakpoints = [700, 960, 1280, 1500];
  const numberOfGamesPerPage = breakpoints.reduce((acc, breakpoint) => {
    if (width > breakpoint) {
      return acc + 1;
    }
    return acc;
  }, 1);

  const isFirstPage = carouselOffset === 0;
  const isLastPage = carouselOffset + numberOfGamesPerPage >= totalNumberOfGames;

  const showPrevPage = () => {
    setCarouselOffset(Math.max(carouselOffset - numberOfGamesPerPage, 0));
  };

  const showNextPage = () => {
    const nextOffset = Math.min(carouselOffset + numberOfGamesPerPage, totalNumberOfGames - numberOfGamesPerPage);
    const needsToFetchMore = nextOffset + numberOfGamesPerPage > games.length;
    const canFetchMore = games.length < totalNumberOfGames;
    if (needsToFetchMore && canFetchMore) {
      setLoading(true);
      fetchGames(games.length)
        .then((data) => {
          setGames([...games, ...data.games]);
          setCarouselOffset(nextOffset);
        }).catch((err) => {
        setError(err.message);
      }).finally(() => setLoading(false));
    } else {
      setCarouselOffset(nextOffset);
    }
  };

  const currentGames = games.slice(carouselOffset, carouselOffset + numberOfGamesPerPage);

  return (
    <Stack spacing={2} direction="column" alignItems="center" sx={{ mt: 4 }}>
      {title && <Typography variant="h4">{title}</Typography>}
      {error && <Alert severity="error">{error}</Alert>}
      {!error && (
        <Stack spacing={2} direction="row" alignItems="center" width={'100%'} justifyContent="center">
          <IconButton size="large" onClick={showPrevPage} disabled={isFirstPage}>
            <ArrowBack/>
          </IconButton>
          <Box sx={{ flexGrow: 1 }}/>
          {loading && [...Array(numberOfGamesPerPage)].map((_, index) => (
            <GameCard key={index}/>
          ))}
          {!loading && currentGames.length === 0 && (
            <Typography variant="h6">No games found</Typography>
          )}
          {!loading && currentGames.map((game) => (
            <GameCard key={game.id} game={game}/>
          ))}
          <Box sx={{ flexGrow: 1 }}/>
          <IconButton size="large" onClick={showNextPage} disabled={isLastPage || loading}>
            <ArrowForward/>
          </IconButton>
        </Stack>
      )}
    </Stack>
  );
};

export default GamesCarousel;
