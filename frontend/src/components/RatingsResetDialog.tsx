import {
  Dialog,
  DialogActions,
  DialogContent,
  DialogContentText,
  DialogTitle,
  Button,
} from '@mui/material';
import { FC } from 'react';
import { db } from '../db/db';

type Props = {
  open: boolean;
  onClose: () => void;
};

const RatingsResetDialog: FC<Props> = ({ open, onClose }) => {
  const handleCancel = () => {
    onClose();
  };

  const handleSave = () => {
    db.ratings.clear();
    onClose();
  };

  return (
    <Dialog open={open}>
      <DialogTitle>Reset ratings</DialogTitle>
      <DialogContent>
        <DialogContentText>
          Are you sure you want to reset all your ratings?
        </DialogContentText>
      </DialogContent>
      <DialogActions>
        <Button onClick={handleCancel}>Cancel</Button>
        <Button onClick={handleSave} variant={'contained'}>Reset</Button>
      </DialogActions>
    </Dialog>
  );
};

export default RatingsResetDialog;
