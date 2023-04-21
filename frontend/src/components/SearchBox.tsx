import { ChangeEvent, FC, useEffect, useState } from 'react';
import { IconButton, InputAdornment, TextField } from '@mui/material';
import SearchIcon from '@mui/icons-material/Search';
import CloseIcon from '@mui/icons-material/Close';

type Props = {
  searchTerm: string;
  setSearchTerm: (searchTerm: string) => void;
};

const SearchBox: FC<Props> = ({searchTerm, setSearchTerm}) => {
  const resetSearchTerm = () => {
    setSearchTerm('');
  };
  
  const handleSearchTermChange = (event: ChangeEvent<HTMLInputElement>) => {
    setSearchTerm(event.target.value);
  };
  
  return (
    <TextField
      label="Search by name"
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
