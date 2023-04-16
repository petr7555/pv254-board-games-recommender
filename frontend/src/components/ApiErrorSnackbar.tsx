import React, { FC } from 'react';
import { Alert, Snackbar } from '@mui/material';
import useError from '../hooks/useError';

const ApiErrorSnackbar: FC = () => {
  const [error, setError] = useError();

  const closeErrorSnackbar = () => {
    setError('');
  };

  return (
    <Snackbar
      anchorOrigin={{ vertical: 'top', horizontal: 'right' }}
      sx={{ marginTop: 5 }}
      autoHideDuration={4000}
      open={Boolean(error)}
      onClose={closeErrorSnackbar}
    >
      <Alert severity="error">
        {error}
      </Alert>
    </Snackbar>
  );
};

export default ApiErrorSnackbar;
