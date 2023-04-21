import { FC, ReactNode } from 'react';
import { Box } from '@mui/material';

type Props = {
  children: ReactNode;
};

const Nonselectable: FC<Props> = ({ children }) => {
  return (
    <Box sx={{ userSelect: 'none' }}>
      {children}
    </Box>
  );
};

export default Nonselectable;
