import { FC } from 'react';
import Card from '@mui/material/Card';
import CardActions from '@mui/material/CardActions';
import CardContent from '@mui/material/CardContent';
import CardMedia from '@mui/material/CardMedia';
import Button from '@mui/material/Button';
import Typography from '@mui/material/Typography';
import Game from '../types/game';
import { Box, Skeleton, Stack } from '@mui/material';
import { ReactComponent as MinAgeIcon } from '../icons/minAgeIcon.svg';
import { ReactComponent as NumPlayersIcon } from '../icons/numPlayersIcon.svg';
import { ReactComponent as PlaytimeIcon } from '../icons/playtimeIcon.svg';
import LabeledIcon from './LabeledIcon';

type Props = {
  game?: Game;
};

const minWidth = 250;
const cardHeight = 500;


const getAmazonSearchUrl = (name: string) => `https://www.amazon.com/s?k=${name}`;

const GameCard: FC<Props> = ({ game }) => {
  if (!game) {
    return (
      <Skeleton variant="rectangular" width={minWidth} height={cardHeight}/>
    );
  }

  return (
    <Card sx={{ minWidth, height: cardHeight, display: 'flex', flexDirection: 'column' }}>
      <CardMedia
        component="img"
        alt={game.name}
        height="140"
        image={game.image}
      />
      <CardContent>
        <Stack direction="column" spacing={1}>
          <Typography gutterBottom variant="h5" component="div">
            {game.name}
          </Typography>
          <Typography variant="body1" color="text.secondary">
            From {game.yearPublished}
          </Typography>
          <Typography variant="body1" color="text.secondary">
            Rating: {Math.round(game.avgRating * 10) / 10} / 10
          </Typography>
          <Typography variant="body1" color="text.secondary">
            Difficulty: {Math.round(game.difficulty * 10) / 10} / 5
          </Typography>
          <LabeledIcon icon={MinAgeIcon} label={`${game.minAge}+`}/>
          <LabeledIcon icon={NumPlayersIcon} label={`${game.minPlayers} - ${game.maxPlayers} players`}/>
          <LabeledIcon icon={PlaytimeIcon} label={`${game.playtime} minutes`}/>
        </Stack>
      </CardContent>
      <Box sx={{ flexGrow: 1 }}/>
      <CardActions sx={{ justifyContent: 'flex-end' }}>
        <Button size="small" variant="outlined">Details</Button>
        <Button size="small" variant="outlined">Rate</Button>
        <Button size="small" variant="outlined"
                href={getAmazonSearchUrl(game.name)} target={'_blank'} sx={{ ml: 1 }}>Buy</Button>
      </CardActions>
    </Card>
  );
};

export default GameCard;
