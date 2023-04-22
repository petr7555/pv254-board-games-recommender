import { useEffect } from 'react';
import { appName } from '../utils/constants';

const usePageTitle = (title: string): void => {
  useEffect(() => {
    document.title = `${title} | ${appName}`;
  }, [title]);
};

export default usePageTitle;
