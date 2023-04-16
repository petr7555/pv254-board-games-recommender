import React from 'react';
import { createBrowserRouter, RouterProvider } from 'react-router-dom';
import HomePage from './components/HomePage';

const router = createBrowserRouter([
  {
    path: '/',
    element: <HomePage/>,
  },
  {
    path: 'about',
    element: <div>About</div>,
  },
]);

const App = () => (
  <RouterProvider router={router}/>
);

export default App;
