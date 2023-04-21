import { rest } from 'msw';
import Game from '../types/game';
import bestGamesByRank from './bestGamesByRank.json';
import GamesSearchRequest from '../types/GamesSearchRequest';
import PagedRequest from '../types/PagedRequest';
import GamesResponse from '../types/GamesResponse';

const getPagedGames = async (allGames: Game[], offset: number, limit: number): Promise<GamesResponse> => {
  const games = allGames.slice(offset, offset + limit);
  const totalNumberOfGames = allGames.length;
  return { games, totalNumberOfGames };
};

const handlers = [
  rest.post('*/recommendations/top-rated', async (req, res, ctx) => {
    const indexedGames = bestGamesByRank.map((game, idx) => {
      return { ...game, name: idx.toString() };
    });
    const { offset, limit }: PagedRequest = await req.json();
    const response = await getPagedGames(bestGamesByRank, offset, limit);

    return res(ctx.delay(300), ctx.status(200), ctx.json(response));
  }),

  rest.post('*/recommendations/most-rated', async (req, res, ctx) => {
    const { offset, limit }: PagedRequest = await req.json();
    const response = await getPagedGames(bestGamesByRank, offset, limit);

    return res(ctx.status(400), ctx.json(response));
  }),

  rest.post('*/recommendations/random', async (req, res, ctx) => {
    const { offset, limit }: PagedRequest = await req.json();
    const response = await getPagedGames(bestGamesByRank, offset, limit);

    return res(ctx.status(200), ctx.json(response));
  }),

  rest.post('*/games', async (req, res, ctx) => {
    const { searchTerm, offset, limit }: GamesSearchRequest = await req.json();
    const matchingGames = bestGamesByRank.filter(game => game.name.toLowerCase().includes(searchTerm.toLowerCase()));
    const response = await getPagedGames(matchingGames, offset, limit);

    return res(ctx.status(200), ctx.json(response));
  }),
];

export default handlers;
