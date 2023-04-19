import React, { FC, useEffect, useState } from 'react';
import axios from 'axios';
import { Alert, Box, IconButton, Stack } from '@mui/material';
import GameCard from './GameCard';
import Game from '../types/game';
import ArrowBack from '@mui/icons-material/ArrowBackIosNew';
import ArrowForward from '@mui/icons-material/ArrowForwardIos';
import { useWindowSize } from 'usehooks-ts';
import RecommendationsResponse from '../types/RecommendationsResponse';

type Props = {
  title: string;
  url: string;
}

const numberOfGamesPerFetch = 10;

const fetchGames = async (url: string, offset: number) => {
  const response = axios.post<RecommendationsResponse>(url, {
    offset,
    limit: 1000,
  });
  const { data } = await response;
  return data;
};

const GamesCarousel: FC<Props> = ({ title, url }) => {
  const { width } = useWindowSize();

  const [error, setError] = useState<string>();
  const [loading, setLoading] = useState(true);

  const [games, setGames] = useState<Game[]>([]);
  // const [totalNumberOfGames, setTotalNumberOfGames] = useState(0);

  const [carouselOffset, setCarouselOffset] = useState(0);

  useEffect(() => {
    fetchGames(url, 0).then((data) => {
      setGames(data.games);
      // setTotalNumberOfGames(data.totalNumberOfGames);
    }).catch((err) => {
      setError(err.message);
    }).finally(() => setLoading(false));
  }, [setError, url]);

  const breakpoints = [700, 960, 1280, 1500];
  const numberOfGamesPerPage = breakpoints.reduce((acc, breakpoint) => {
    if (width > breakpoint) {
      return acc + 1;
    }
    return acc;
  }, 1);

  const isFirstPage = carouselOffset === 0;
  const isLastPage = carouselOffset + numberOfGamesPerPage >= games.length;

  // const numberOfFetchedGames = games.length;
  // const fetchedAllGames = numberOfFetchedGames >= totalNumberOfGames;

  const showPrevPage = () => {
    setCarouselOffset(Math.max(carouselOffset - numberOfGamesPerPage, 0));
  };

  const showNextPage = () => {
    setCarouselOffset(Math.min(carouselOffset + numberOfGamesPerPage, games.length - numberOfGamesPerPage));

    // const needsToFetchMoreGames = !fetchedAllGames && numberOfFetchedGames >= games.length;
    // if (isLastPage) {
    //   setLoading(true);
    //   fetchGames(url, currentPage * numberOfGamesPerPage).then((data) => {
    //     setGames([...games, ...data.games]);
    //     setTotalNumberOfGames(data.totalNumberOfGames);
    //   }).catch(setError)
    //     .finally(() => setLoading(false));
    //
    //   setCurrentPage(currentPage + 1);
    // }
  };

  const currentGames = games.slice(carouselOffset, carouselOffset + numberOfGamesPerPage);

  return (
    <Stack spacing={2} direction="column" alignItems="center">
      <h1>{title}</h1>
      {error && <Alert severity="error">{error}</Alert>}
      {!error && (
        <Stack spacing={2} direction="row" alignItems="center" width={"100%"} justifyContent="center">
          <IconButton size="large" onClick={showPrevPage} disabled={isFirstPage}>
            <ArrowBack/>
          </IconButton>
          <Box sx={{ flexGrow: 1 }}/>
          {loading && [...Array(numberOfGamesPerPage)].map((_, index) => (
            <GameCard key={index}/>
          ))}
          {!loading && currentGames.map((game) => (
            <GameCard key={game.id} game={game}/>
          ))}
          <Box sx={{ flexGrow: 1 }}/>
          <IconButton size="large" onClick={showNextPage} disabled={isLastPage}>
            <ArrowForward/>
          </IconButton>
        </Stack>
      )}
    </Stack>
  );
};

export default GamesCarousel;
