import { FC, useState } from 'react';
import usePageTitle from '../../hooks/usePageTitle';
import { useLiveQuery } from 'dexie-react-hooks';
import { db } from '../../db/db';
import { Rating, Stack } from '@mui/material';
import Button from '@mui/material/Button';
import Nonselectable from '../Nonselectable';
import { DataGrid, GridColDef } from '@mui/x-data-grid';
import SearchBox from '../SearchBox';
import RatingsResetDialog from '../RatingsResetDialog';

const columns: GridColDef[] = [
  {
    field: 'name',
    flex: 1,
    renderHeader: () => <Nonselectable>Name</Nonselectable>,
    valueGetter: (params) => params.row.game.name
  },
  {
    field: 'image',
    flex: 1,
    sortable: false,
    renderHeader: () => <Nonselectable>Image</Nonselectable>,
    renderCell: (params) => <img src={params.row.game.image} alt={params.row.game.name}
                                 style={{ objectFit: 'cover', width: '100%', height: '100%' }}/>
  },
  {
    field: 'value',
    flex: 1,
    renderHeader: () => <Nonselectable>Your rating</Nonselectable>,
    renderCell: (params) => <Rating value={params.row.value} precision={0.5} readOnly/>
  },
  {
    field: 'updatedAt',
    flex: 1,
    renderHeader: () => <Nonselectable>Rating given at</Nonselectable>,
    renderCell: (params) => new Date(params.row.updatedAt).toLocaleString()
  },
];

const MyRatings: FC = () => {
  usePageTitle('My ratings');

  const [searchTerm, setSearchTerm] = useState('');

  const ratings = useLiveQuery(() => db.ratings.orderBy('updatedAt').reverse().toArray()) ?? [];
  const ratingsWithIds = ratings.map((rating) => ({ id: rating.gameId, ...rating }));
  const filteredRatings = ratingsWithIds.filter((rating) => rating.game.name.toLowerCase().includes(searchTerm.toLowerCase()));

  const [dialogOpen, setDialogOpen] = useState(false);
  const openDialog = () => {
    setDialogOpen(true);
  };
  const closeDialog = () => {
    setDialogOpen(false);
  };

  return (
    <Stack spacing={2} sx={{ pt: 3 }}>
      <SearchBox searchTerm={searchTerm} setSearchTerm={setSearchTerm}/>
      <Button variant={'contained'} sx={{ alignSelf: 'flex-end' }} onClick={openDialog}>Reset ratings</Button>
      <RatingsResetDialog open={dialogOpen} onClose={closeDialog}/>
      <DataGrid
        rows={filteredRatings}
        columns={columns}
        rowHeight={200}
        disableColumnMenu={true}
        disableRowSelectionOnClick={true}
      />
    </Stack>
  );
};

export default MyRatings;
