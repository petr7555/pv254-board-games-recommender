import {
  Dialog,
  DialogActions,
  DialogContent,
  DialogContentText,
  DialogTitle,
  Rating,
  Button,
} from '@mui/material';
import { ChangeEvent, FC, useEffect, useState } from 'react';
import Game from '../types/Game';
import { db } from '../db/db';
import { useLiveQuery } from 'dexie-react-hooks';
import { maxRatingValue } from '../utils/constants';

type Props = {
  game: Game;
  open: boolean;
  onClose: () => void;
};

const RatingDialog: FC<Props> = ({ game, open, onClose }) => {
  const savedRating = useLiveQuery(() => db.ratings.get(game.id), [game.id]);
  const defaultRatingValue = savedRating?.value ?? 0;
  const [newRatingValue, setNewRatingValue] = useState(defaultRatingValue);

  useEffect(() => {
    setNewRatingValue(defaultRatingValue);
  }, [defaultRatingValue]);

  const handleCancel = () => {
    onClose();
    setNewRatingValue(defaultRatingValue);
  };

  const handleSave = async () => {
    onClose();

    await db.ratings.put({
      gameId: game.id,
      game,
      value: newRatingValue,
      updatedAt: new Date(),
    });
  };

  const onRatingChange = (event: ChangeEvent<{}>, newValue: number | null) => {
    if (newValue !== null) {
      setNewRatingValue(newValue);
    }
  };

  return (
    <Dialog open={open}>
      <DialogTitle>Rate {game.name}</DialogTitle>
      <DialogContent>
        <DialogContentText>
          How much did you enjoy {game.name}?
        </DialogContentText>
        <Rating
          value={newRatingValue}
          onChange={onRatingChange}
          max={maxRatingValue}
        />
      </DialogContent>
      <DialogActions>
        <Button onClick={handleCancel}>Cancel</Button>
        <Button onClick={handleSave} variant={'contained'}>Save</Button>
      </DialogActions>
    </Dialog>
  );
};

export default RatingDialog;
