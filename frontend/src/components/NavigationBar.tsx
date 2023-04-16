import { AppBar, Tab, Tabs } from '@mui/material';
import React, { FC, SyntheticEvent, useState } from 'react';
import { Link } from 'react-router-dom';

const pages = [
  {
    name: 'Recommendations',
    path: '/',
  },
  {
    name: 'My ratings',
    path: '/my-ratings',
  },
];

const NavigationBar: FC = () => {
  const [selectedTab, setSelectedTab] = useState(0);

  const handleChange = (event: SyntheticEvent, newValue: number) => {
    setSelectedTab(newValue);
  };

  return (
    <AppBar position="sticky">
      <Tabs value={selectedTab} onChange={handleChange}
            indicatorColor="secondary" textColor="inherit" variant="fullWidth">
        {pages.map(({ name, path }) => (
          <Tab key={name} label={name} component={Link} to={path}/>
        ))}
      </Tabs>
    </AppBar>
  );
};

export default NavigationBar;
