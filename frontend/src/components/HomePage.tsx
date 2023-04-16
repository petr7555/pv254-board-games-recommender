import { Link } from 'react-router-dom';
import React, { FC } from 'react';

const HomePage: FC = () => {
  return (
    <div>
      <h1>Hello World</h1>
      <Link to="about">About Us</Link>
    </div>
  );
};

export default HomePage;
