import { rest, RestRequest } from 'msw';
import Game from '../types/game';
import bestGamesByRank from './bestGamesByRank.json';
import RecommendationsRequest from '../types/RecommendationsRequest';
import RecommendationsResponse from '../types/RecommendationsResponse';

const getPagedGamesFromRequest = async (allGames: Game[], request: RestRequest): Promise<RecommendationsResponse> => {
  const { offset, limit }: RecommendationsRequest = await request.json();
  const games = allGames.slice(offset, offset + limit);
  const totalNumberOfGames = allGames.length;
  return { games, totalNumberOfGames };
};

const handlers = [
  rest.post('*/recommendations/top-rated', async (req, res, ctx) => {
    const indexedGames = bestGamesByRank.map((game, idx) => {
      return { ...game, name: idx.toString() };
    });
    const response = await getPagedGamesFromRequest(bestGamesByRank, req);

    return res(ctx.delay(300), ctx.status(200), ctx.json(response));
  }),

  rest.post('*/recommendations/most-rated', async (req, res, ctx) => {
    const response = await getPagedGamesFromRequest(bestGamesByRank, req);

    return res(ctx.status(400), ctx.json(response));
  }),

  rest.post('*/recommendations/random', async (req, res, ctx) => {
    const response = await getPagedGamesFromRequest(bestGamesByRank, req);

    return res(ctx.status(200), ctx.json(response));
  }),
];

export default handlers;
