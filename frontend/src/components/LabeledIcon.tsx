import { FC } from 'react';
import { ReactComponent } from '*.svg';
import { Stack } from '@mui/material';
import Typography from '@mui/material/Typography';

type Props = {
  icon: typeof ReactComponent;
  label: string;
};

const LabeledIcon: FC<Props> = ({ icon: Icon, label }) => {
  return (<Stack direction="row" spacing={1} alignItems="center">
    <Icon style={{ width: 30, height: 30 }}/>
    <Typography variant="body1" color="text.secondary">
      {label}
    </Typography>
  </Stack>);
};

export default LabeledIcon;
