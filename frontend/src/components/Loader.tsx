import React, { FC } from 'react';
import { Backdrop, CircularProgress } from '@mui/material';
import useLoader from '../hooks/useLoader';

const Loader: FC = () => {
  const [loading] = useLoader();

  return (
    <Backdrop sx={{ color: 'primary.main', zIndex: (theme) => theme.zIndex.drawer + 1 }} open={loading}>
      <CircularProgress color="inherit"/>
    </Backdrop>
  );
};

export default Loader;
