const getApiUrl = (): string => {
  if (process.env.NODE_ENV === 'development') {
    return 'http://localhost:8000';
  }
  // TODO add production server URL
  throw new Error('Not implemented');
};

export default getApiUrl;
