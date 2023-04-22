import { BrowserRouter } from 'react-router-dom';
import theme from './utils/theme';
import { CssBaseline, ThemeProvider } from '@mui/material';
import Layout from './components/Layout';
import RoutesSwitch from './components/RoutesSwitch';

const App = () => (
  <>
    <CssBaseline/>
    <ThemeProvider theme={theme}>
      <BrowserRouter>
        <Layout>
          <RoutesSwitch/>
        </Layout>
      </BrowserRouter>
    </ThemeProvider>
  </>
);

export default App;
