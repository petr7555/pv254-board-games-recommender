import { FC, ReactNode } from 'react';
import { Container } from '@mui/material';
import NavigationBar from './NavigationBar';

type Props = {
  children: ReactNode;
};

const Layout: FC<Props> = ({ children }) => {
  return (
    <>
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
