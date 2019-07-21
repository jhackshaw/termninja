import React from 'react';
import { ListGroup,
         ListGroupItem } from 'reactstrap';
import classes from './GamesList.css';


const GamesList = ({ rounds }) => {

  return (
    <ListGroup>
      { rounds.map(round => (
        <ListGroupItem key={round.id} className={classes.item}>
          <a className="d-flex text-secondary">
            <div className={classes.column}>{ round.played_at }</div>
            <div className={classes.column}>{ round.user_}</div>
            <div className={classes.column}>{ round.score }</div>
            <div className={classes.mainColumn}>{ game.server_name }</div>
            <div className={classes.column}>{ game.port }</div>
          </a>
        </ListGroupItem>
      ))}
    </ListGroup>
  )
}

export default GamesList;
