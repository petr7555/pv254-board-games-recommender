import { FC } from 'react';
import { Stack, Typography } from '@mui/material';
// eslint-disable-next-line import/no-unresolved
import { ReactComponent } from '*.svg';

type Props = {
  icon: typeof ReactComponent;
  label: string;
};

const LabeledIcon: FC<Props> = ({ icon: Icon, label }) => {
  return (
    <Stack direction="row" spacing={1} alignItems="center">
      <Icon style={{ width: 30, height: 30 }} />
      <Typography variant="body1" color="text.secondary">
        {label}
      </Typography>
    </Stack>
  );
};

export default LabeledIcon;
