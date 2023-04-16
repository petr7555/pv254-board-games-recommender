import React, { FC } from 'react';
import usePageTitle from '../../hooks/usePageTitle';

const Recommendations: FC = () => {
  usePageTitle('Recommendations');
  
  return (
    <div>
      <h1>Recommendations</h1>
    </div>
  );
};

export default Recommendations;
