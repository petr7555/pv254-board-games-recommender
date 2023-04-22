import { developmentServerUrl, productionServerUrl } from './constants';

const getApiUrl = (): string => {
  if (process.env.NODE_ENV === 'development') {
    return developmentServerUrl;
  }
  return productionServerUrl;
};

export default getApiUrl;
