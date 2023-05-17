import PagedRequest from './PagedRequest';

type GamesSearchRequest = PagedRequest & {
  searchTerm: string;
};

export default GamesSearchRequest;
