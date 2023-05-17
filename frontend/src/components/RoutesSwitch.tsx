import { FC } from 'react';
import { Navigate, Route, Routes } from 'react-router-dom';
import Recommendations from './pages/Recommendations';
import MyRatings from './pages/MyRatings';
import { myRatingsPath, recommendationsPath } from '../utils/constants';

const RoutesSwitch: FC = () => (
  <Routes>
    <Route path={recommendationsPath} element={<Recommendations />} />
    <Route path={myRatingsPath} element={<MyRatings />} />
    <Route path="*" element={<Navigate replace to={recommendationsPath} />} />
  </Routes>
);

export default RoutesSwitch;
