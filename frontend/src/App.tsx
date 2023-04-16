import React from 'react';
import { BrowserRouter } from 'react-router-dom';
import theme from './utils/theme';
import { CssBaseline, ThemeProvider } from '@mui/material';
import Layout from './components/Layout';
import { LoaderProvider } from './hooks/useLoader';
import { ErrorProvider } from './hooks/useError';
import RoutesSwitch from './components/RoutesSwitch';

const App = () => (
  <>
    <CssBaseline/>
    <ThemeProvider theme={theme}>
      <ErrorProvider>
        <LoaderProvider>
          <BrowserRouter>
            <Layout>
              <RoutesSwitch/>
            </Layout>
          </BrowserRouter>
        </LoaderProvider>
      </ErrorProvider>
    </ThemeProvider>
  </>
);

export default App;
