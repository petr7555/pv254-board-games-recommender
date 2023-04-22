import React, { FC } from 'react';
import { Navigate, Route, Routes } from 'react-router-dom';
import Recommendations from './pages/Recommendations';
import MyRatings from './pages/MyRatings';

const RoutesSwitch: FC = () => (
  <Routes>
    <Route path="/" element={<Recommendations/>}/>
    <Route path="/my-ratings" element={<MyRatings/>}/>
    <Route path="*" element={<Navigate replace to="/"/>}/>
  </Routes>
);

export default RoutesSwitch;
