const getApiUrl = (): string => {
  if (process.env.NODE_ENV === 'development') {
    return 'http://localhost:8000';
  }
  return 'https://pv254-board-games-recommender-server.onrender.com';
};

export default getApiUrl;
