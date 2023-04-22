import React, { ChangeEvent, FC, useState } from 'react';
import usePageTitle from '../../hooks/usePageTitle';
import { useLiveQuery } from 'dexie-react-hooks';
import { db } from '../../db/db';
import { Rating, Stack } from '@mui/material';
import Button from '@mui/material/Button';
import Nonselectable from '../Nonselectable';
import { DataGrid, GridColDef } from '@mui/x-data-grid';
import SearchBox from '../SearchBox';
import RatingsResetDialog from '../RatingsResetDialog';
import RateGamesDialog from '../RateGamesDialog';
import GameRating from '../../types/GameRating';
import { maxRatingValue } from '../../utils/constants';
import Typography from '@mui/material/Typography';
import ImageWithSkeleton from '../ImageWithSkeleton';

const rowHeight = 150;

const MyRatings: FC = () => {
  usePageTitle('My ratings');

  const [page, setPage] = useState(0);
  const [pageSize, setPageSize] = useState(3);

  const [searchTerm, setSearchTerm] = useState('');

  const dbRatings = useLiveQuery(() => db.ratings.orderBy('updatedAt').reverse().toArray());
  const dbRatingsLoading = dbRatings === undefined;
  const ratings = dbRatings ?? [];
  const filteredRatings = ratings.filter((rating) => rating.game.name.toLowerCase().includes(searchTerm.toLowerCase()));

  const [resetDialogOpen, setResetDialogOpen] = useState(false);
  const openResetDialog = () => {
    setResetDialogOpen(true);
  };
  const closeResetDialog = () => {
    setResetDialogOpen(false);
  };

  const [rateGamesDialogOpen, setRateGamesDialogOpen] = useState(false);
  const openRateGamesDialog = () => {
    setRateGamesDialogOpen(true);
  };
  const closeRateGamesDialog = () => {
    setRateGamesDialogOpen(false);
  };

  const onRatingChange = (event: ChangeEvent<{}>, newValue: number | null, rating: GameRating) => {
    if (newValue !== null) {
      db.ratings.put({
        ...rating,
        value: newValue,
        updatedAt: new Date(),
      });
    }
  };

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
      renderCell: (params) => <ImageWithSkeleton image={params.row.game.image} alt={params.row.game.name}
                                                 height={rowHeight}/>
    },
    {
      field: 'value',
      flex: 1,
      renderHeader: () => <Nonselectable>Your rating</Nonselectable>,
      renderCell: (params) => <Rating value={params.row.value} max={maxRatingValue}
                                      onChange={(event, value) => onRatingChange(event, value, params.row)}/>
    },
    {
      field: 'updatedAt',
      flex: 1,
      renderHeader: () => <Nonselectable>Rating given at</Nonselectable>,
      renderCell: (params) => new Date(params.row.updatedAt).toLocaleString()
    },
  ];

  return (
    <Stack spacing={2} sx={{ pt: 3 }}>
      <SearchBox label={'Search my ratings by name'} searchTerm={searchTerm} setSearchTerm={setSearchTerm}/>
      <Stack direction={'row'} sx={{ justifyContent: 'space-between' }}>
        <Button variant={'contained'} onClick={openRateGamesDialog}>Rate games</Button>
        <Button variant={'contained'} onClick={openResetDialog}>Reset ratings</Button>
      </Stack>
      <RateGamesDialog open={rateGamesDialogOpen} onClose={closeRateGamesDialog}/>
      <RatingsResetDialog open={resetDialogOpen} onClose={closeResetDialog}/>
      {!dbRatingsLoading && ratings.length === 0 &&
        <Typography variant="h6" align={'center'}>Press "Rate games" to get started</Typography>}
      {ratings.length > 0 && filteredRatings.length === 0 &&
        <Typography variant="h6" align={'center'}>No ratings found for given search term</Typography>}
      {filteredRatings.length > 0 && (<DataGrid
        rows={filteredRatings}
        columns={columns}
        rowHeight={rowHeight}
        disableColumnMenu={true}
        disableRowSelectionOnClick={true}
        getRowId={(row) => row.gameId}
        pageSizeOptions={[3, 5, 10]}
        paginationModel={{
          page,
          pageSize,
        }}
        onPaginationModelChange={(params) => {
          setPage(params.page);
          setPageSize(params.pageSize);
        }}
      />)}
    </Stack>
  );
};

export default MyRatings;
