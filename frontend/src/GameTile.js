import React from 'react';
import { Card,
         CardHeader,
         CardMedia,
         CardContent, 
         Avatar,
         Typography} from '@material-ui/core';
import { makeStyles } from '@material-ui/styles';


const useStyles = makeStyles(theme => ({
  media: {
    minWidth: '20%'
  },
  root: {
    display: 'flex',
    margin: theme.spacing(2),
    padding: theme.spacing(2),
    [theme.breakpoints.down('sm')]: {
      marginRight: 0,
      marginLeft: 0
    }
  },
  contentRoot: {
    display: 'flex',
    flexDirection: 'column',
    padding: theme.spacing(1)
  }
}))

const GameTile = ({ name, description, image, url, port }) => {
  const classes = useStyles()

  return (
    <Card classes={{root: classes.root}}>
      <CardMedia
        className={ classes.media }
        image={ `/static/images/${image}` }
        title={ name }
      />
      <CardContent classes={{root: classes.contentRoot}}>
        <Typography variant="h6" noWrap>
          { name }
        </Typography>
        <Typography variant="body1" color="textSecondary" component="p" noWrap>
          { description }
        </Typography>
      </CardContent>
    </Card>
  )
}

export default GameTile;
