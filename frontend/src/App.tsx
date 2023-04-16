import React from 'react';
import { createBrowserRouter, RouterProvider } from 'react-router-dom';
import HomePage from './components/HomePage';
import theme from './utils/theme';
import { ThemeProvider } from '@mui/system';

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
  <ThemeProvider theme={theme}>
    <RouterProvider router={router}/>
  </ThemeProvider>
);

export default App;
