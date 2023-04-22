import { rest } from 'msw';
import Game from '../types/Game';
import gamesOrderedByNameMock from './data/gamesOrderedByNameMock.json';
import gamesOrderedByRankMock from './data/gamesOrderedByRankMock.json';
import gamesOrderedByNumberOfRatingsMock from './data/gamesOrderedByNumberOfRatingsMock.json';
import GamesSearchRequest from '../types/GamesSearchRequest';
import PagedRequest from '../types/PagedRequest';
import GamesResponse from '../types/GamesResponse';
import PersonalizedRecommendationsRequest from '../types/PersonalizedRecommendationsRequest';

const getPagedGames = async (allGames: Game[], offset: number, limit: number): Promise<GamesResponse> => {
  const games = allGames.slice(offset, offset + limit);
  const totalNumberOfGames = allGames.length;
  return { games, totalNumberOfGames };
};

const random = (seed: number) => {
  const x = Math.sin(seed) * 10000;
  return x - Math.floor(x);
};

const handlers = [
  rest.post('*/recommendations/personalized', async (req, res, ctx) => {
    const { ratings, offset, limit }: PersonalizedRecommendationsRequest = await req.json();
    let seed = ratings.reduce((acc, rating) => acc + (rating.gameId * rating.value), 0);
    const shuffledGames = [...gamesOrderedByNameMock].sort(() => 0.5 - random(seed++));
    const response = await getPagedGames(shuffledGames, offset, limit);

    return res(ctx.status(200), ctx.json(response));
  }),

  rest.post('*/recommendations/top-rated', async (req, res, ctx) => {
    const { offset, limit }: PagedRequest = await req.json();
    const response = await getPagedGames(gamesOrderedByRankMock, offset, limit);

    return res(ctx.delay(300), ctx.status(200), ctx.json(response));
  }),

  rest.post('*/recommendations/most-rated', async (req, res, ctx) => {
    const { offset, limit }: PagedRequest = await req.json();
    const response = await getPagedGames(gamesOrderedByNumberOfRatingsMock, offset, limit);

    return res(ctx.status(200), ctx.json(response));
  }),

  rest.post('*/recommendations/random', async (req, res, ctx) => {
    const { offset, limit }: PagedRequest = await req.json();
    const shuffledGames = [...gamesOrderedByNameMock].sort(() => 0.5 - Math.random());
    const response = await getPagedGames(shuffledGames, offset, limit);

    return res(ctx.status(200), ctx.json(response));
  }),

  rest.post('*/games', async (req, res, ctx) => {
    const { searchTerm, offset, limit }: GamesSearchRequest = await req.json();
    const matchingGames = gamesOrderedByNameMock.filter(game => game.name.toLowerCase().includes(searchTerm.toLowerCase()));
    const response = await getPagedGames(matchingGames, offset, limit);

    return res(ctx.status(200), ctx.json(response));
  }),
];

export default handlers;
