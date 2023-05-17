import { AppBar, Tab, Tabs } from '@mui/material';
import { FC, SyntheticEvent, useState } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { myRatingsPath, recommendationsPath } from '../utils/constants';

const pages = [
  {
    name: 'Recommendations',
    path: recommendationsPath,
  },
  {
    name: 'My ratings',
    path: myRatingsPath,
  },
];

const NavigationBar: FC = () => {
  const location = useLocation();

  const [selectedTab, setSelectedTab] = useState(
    pages.findIndex(({ path }) => path === location.pathname),
  );

  const handleChange = (event: SyntheticEvent, newValue: number) => {
    setSelectedTab(newValue);
  };

  return (
    <AppBar position="sticky">
      <Tabs
        value={selectedTab}
        onChange={handleChange}
        indicatorColor="secondary"
        textColor="inherit"
        variant="fullWidth"
      >
        {pages.map(({ name, path }) => (
          <Tab key={name} label={name} component={Link} to={path} />
        ))}
      </Tabs>
    </AppBar>
  );
};

export default NavigationBar;
