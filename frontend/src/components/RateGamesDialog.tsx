import { Box, Dialog, DialogContent, DialogTitle, IconButton } from '@mui/material';
import { FC, useState } from 'react';
import SearchBox from './SearchBox';
import GamesCarousel from './GamesCarousel';
import { Close as CloseIcon } from '@mui/icons-material';
import { useDebounce } from 'usehooks-ts';
import { debounceDelay, gamesEndpoint } from '../utils/constants';

type Props = {
  open: boolean;
  onClose: () => void;
};

const RateGamesDialog: FC<Props> = ({ open, onClose }) => {
  const [searchTerm, setSearchTerm] = useState('');
  const debouncedSearchTerm = useDebounce(searchTerm, debounceDelay);

  const handleClose = () => {
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
        <SearchBox label={'Search all games by name'} searchTerm={searchTerm} setSearchTerm={setSearchTerm}/>
        <GamesCarousel url={gamesEndpoint} searchTerm={debouncedSearchTerm}/>
      </DialogContent>
    </Dialog>
  );
};

export default RateGamesDialog;
