import React from "react";
import { ListGroup, ListGroupItem, Row, Col } from "reactstrap";
import classes from "./GamesList.css";
import Link from "next/link";

const isOnline = (game) => true;

const GamesList = ({ games }) => {
  return (
    <ListGroup>
      <ListGroupItem className={`${classes.header} d-flex`} tag={Row}>
        <Col xs={2} className="text-center">
          Status
        </Col>
        <Col xs={8}>Name</Col>
        <Col xs={2} className="text-center">
          Number
        </Col>
      </ListGroupItem>
      {games.map((game) => (
        <ListGroupItem key={game.slug} className={classes.item} tag={Row}>
          <Link href="/g/[gameSlug]" as={`/g/${game.slug}`}>
            <a className="d-flex text-secondary">
              <Col xs={2} className="text-center">
                <i
                  className={`fas fa-lg fa-circle ${
                    isOnline(game) ? classes.online : classes.offline
                  }`}
                />
              </Col>
              <Col xs={8}>{game.name}</Col>
              <Col xs={2} className="text-center">
                {game.idx}
              </Col>
            </a>
          </Link>
        </ListGroupItem>
      ))}
    </ListGroup>
  );
};

export default GamesList;
