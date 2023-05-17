import { BrowserRouter } from 'react-router-dom';
import { ThemeProvider, CssBaseline } from '@mui/material';
import { FC } from 'react';
import theme from './utils/theme';
import Layout from './components/Layout';
import RoutesSwitch from './components/RoutesSwitch';

const App: FC = () => {
  return (
    <>
      <CssBaseline />
      <ThemeProvider theme={theme}>
        <BrowserRouter>
          <Layout>
            <RoutesSwitch />
          </Layout>
        </BrowserRouter>
      </ThemeProvider>
    </>
  );
};

export default App;
