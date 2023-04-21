import { Box, Dialog, DialogContent, DialogTitle, IconButton } from '@mui/material';
import React, { FC, useState } from 'react';
import SearchBox from './SearchBox';
import GamesCarousel from './GamesCarousel';
import CloseIcon from '@mui/icons-material/Close';

type Props = {
  open: boolean;
  onClose: () => void;
};

const AddRatingDialog: FC<Props> = ({ open, onClose }) => {
  const [searchTerm, setSearchTerm] = useState('');

  const handleClose = () => {
    onClose();
  };

  const handleSave = () => {
    // db.ratings.clear();
    onClose();
  };

  return (
    <Dialog open={open} fullScreen>
      <DialogTitle>Rate games
        <IconButton
          onClick={handleClose}
          sx={{
            position: 'absolute',
            right: 8,
            top: 8,
          }}
        >
          <CloseIcon/>
        </IconButton>
      </DialogTitle>
      <DialogContent>
        <Box sx={{ height: 10 }}/>
        <SearchBox searchTerm={searchTerm} setSearchTerm={setSearchTerm}/>
        <GamesCarousel title={''} url={'/games'} additionalBodyParams={{ searchTerm }}/>
      </DialogContent>
    </Dialog>
  );
};

export default AddRatingDialog;
