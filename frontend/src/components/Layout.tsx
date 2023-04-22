import { FC, ReactNode } from 'react';
import { Container } from '@mui/material';
import ApiErrorSnackbar from './ApiErrorSnackbar';
import Loader from './Loader';
import NavigationBar from './NavigationBar';

type Props = {
  children: ReactNode;
};

const Layout: FC<Props> = ({ children }) => {
  return (
    <>
      <Loader/>
      <ApiErrorSnackbar/>
      <NavigationBar/>
      <Container
        maxWidth="lg"
        component="main"
        sx={{
          pb: 8,
        }}
      >
        {children}
      </Container>
    </>
  );
};

export default Layout;
