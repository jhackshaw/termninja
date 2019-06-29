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
    height: 0,
    paddingTop: '56.25%'
  },
  root: {
    height: '100%'
  }
}))

const GameTile = ({ name, description, image, url, port }) => {
  const classes = useStyles()

  return (
    <Card classes={{root: classes.root}}>
      <CardHeader
        avatar={ <Avatar>{ name[0] }</Avatar> }
        title={ name }
      />
      <CardMedia
        className={classes.media}
        image={ `/static/images/${image}` }
        title={ name }
      />
      <CardContent>
        <Typography variant="body1" color="textSecondary" component="p">
          { description }
        </Typography>
      </CardContent>
    </Card>
  )
}

export default GameTile;
