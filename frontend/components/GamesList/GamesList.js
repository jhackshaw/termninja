import React from 'react';
import { ListGroup,
         ListGroupItem } from 'reactstrap';
import classes from './GamesList.css';
import Link from 'next/link';

const isOnline = game => true; 

const GamesList = ({ games }) => {

  return (
    <ListGroup>
      { games.map(game => (
        <ListGroupItem key={game.slug} className={classes.item}>
            <Link href="/g/[gameSlug]" as={`/g/${game.slug}`}>
            <a className="d-flex text-secondary">
              <div className={classes.column}>
                  <i className={`fas fa-lg fa-circle ${isOnline(game) ? classes.online : classes.offline}`} />
              </div>
              <div className={classes.mainColumn}>{ game.server_name }</div>
              <div className={classes.column}>{ game.port }</div>
            </a>
          </Link>
        </ListGroupItem>
      ))}
    </ListGroup>
  )
}

export default GamesList;
