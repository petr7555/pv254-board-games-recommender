import { Dialog, DialogActions, DialogContent, DialogContentText, DialogTitle, Rating } from '@mui/material';
import Button from '@mui/material/Button';
import React, { FC, useState } from 'react';
import Game from '../types/game';
import { useLocalStorage } from 'usehooks-ts';

type Props = {
  game: Game;
  open: boolean;
  onClose: () => void;
};

const RatingDialog: FC<Props> = ({ game, open, onClose }) => {
  const [savedRating, setSavedRating] = useLocalStorage<number | null>(`rating-${game?.id}`, null);
  const [newRating, setNewRating] = useState(savedRating);

  const handleCancel = () => {
    onClose();
    setNewRating(savedRating);
  };

  const handleSave = () => {
    onClose();
    setSavedRating(newRating);
  };

  return (
    <Dialog open={open}>
      <DialogTitle>Rate {game.name}</DialogTitle>
      <DialogContent>
        <DialogContentText>
          How much did you enjoy {game.name}?
        </DialogContentText>
        <Rating
          name="rating"
          value={newRating}
          precision={0.5}
          onChange={(event, newValue) => {
            if (newValue !== null) {
              setNewRating(newValue);
            }
          }}
        />
      </DialogContent>
      <DialogActions>
        <Button onClick={handleCancel}>Cancel</Button>
        <Button onClick={handleSave} variant={'contained'}>Save</Button>
      </DialogActions>
    </Dialog>);
};

export default RatingDialog;
