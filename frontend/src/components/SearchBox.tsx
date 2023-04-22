import { ChangeEvent, FC } from 'react';
import { IconButton, InputAdornment, TextField } from '@mui/material';
import SearchIcon from '@mui/icons-material/Search';
import CloseIcon from '@mui/icons-material/Close';

type Props = {
  label: string;
  searchTerm: string;
  setSearchTerm: (searchTerm: string) => void;
};

const SearchBox: FC<Props> = ({ label, searchTerm, setSearchTerm }) => {
  const resetSearchTerm = () => {
    setSearchTerm('');
  };

  const handleSearchTermChange = (event: ChangeEvent<HTMLInputElement>) => {
    setSearchTerm(event.target.value);
  };

  return (
    <TextField
      label={label}
      fullWidth
      InputProps={{
        startAdornment: (
          <InputAdornment position="start">
            <SearchIcon/>
          </InputAdornment>
        ),
        endAdornment: (
          <InputAdornment position="end">
            <IconButton onClick={resetSearchTerm}>
              <CloseIcon/>
            </IconButton>
          </InputAdornment>
        ),
      }}
      value={searchTerm}
      onChange={handleSearchTermChange}
    />
  );
};

export default SearchBox;
