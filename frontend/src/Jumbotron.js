import React from 'react';
import { makeStyles } from '@material-ui/styles';
import { Typography, Grid, Hidden, CardMedia, Card } from '@material-ui/core';


const useStyles = makeStyles(theme => ({
  root: {
    height: '40vh',
    backgroundImage: "url(/static/images/header_background.svg)",
    backgroundSize: 'cover',
    backgroundRepeat: 'no-repeat',
    color: 'white'
  },
  logoWrapper:{
    height: '30%'
  },
  logo: {
    height: 0,
    paddingTop: '56.25%'
  }
}))


const Jumbotron = props => {
  const classes = useStyles()

  return (
    <Grid container justify="center" alignContent="center" alignItems="center" classes={{container: classes.root}}>
      <Grid item xs={11} sm={6} md={5} lg={4} xl={3}>
        <Typography variant="h2" color="inherit" align="left" gutterBottom>
          TermNinja
        </Typography>
        <Typography variant="body1" color="inherit" align="left">
          Simple games played right in your terminal.
        </Typography>
      </Grid>
      <Hidden xsDown>
        <Grid item sm={4} md={3} lg={3} xl={2}>
          <Card>
            <CardMedia
              image={"/static/images/logo.jpg"}
              className={classes.logo}
            />
          </Card>
        </Grid>
      </Hidden>
    </Grid>
  )
}

export default Jumbotron;
