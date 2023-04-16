import { useEffect } from 'react';

const usePageTitle = (title: string): void => {
  useEffect(() => {
    document.title = `${title} | Board games recommender`;
  }, [title]);
};

export default usePageTitle;
