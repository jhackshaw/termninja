import React from 'react';
import { makeStyles } from '@material-ui/core/styles';
import AppBar from '@material-ui/core/AppBar';
import Toolbar from '@material-ui/core/Toolbar';
import Typography from '@material-ui/core/Typography';
import CodeIcon from '@material-ui/icons/Code';


const useStyles = makeStyles(theme => ({
  root: {
    flexGrow: 1,
  },
  title: {
    fontFamily: 'Ubuntu',
    flexGrow: 1,
  },
}));

const Navbar = props => {
  const classes = useStyles();

  return (
    <div className={classes.root}>
      <AppBar position="static" color="default">
        <Toolbar variant="dense">
          <CodeIcon color="primary" /> 
          <Typography variant="h6" color="primary" className={classes.title}>
            TermNinja
          </Typography>
        </Toolbar>
      </AppBar>
    </div>
  );
}

export default Navbar;
