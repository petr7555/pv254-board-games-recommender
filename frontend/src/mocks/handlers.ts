import { rest } from 'msw';

const handlers = [
  rest.post('*/image', (req, res, ctx) => {
    return res(ctx.status(200), ctx.json(
      {
        id: '52179-B0169RSNPG',
        image: 'https://m.media-amazon.com/images/I/41UcPfrmzVL._SL500_.jpg',
      }
    ));
  }),
];

export default handlers;
