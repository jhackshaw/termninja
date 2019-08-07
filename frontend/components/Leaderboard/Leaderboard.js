import React from 'react';
import Link from 'next/link';
import { ListGroup,
         ListGroupItem,
         Row,
         Col } from 'reactstrap';
import classes from './Leaderboard.css';


const Leaderboard = ({ leaders }) => {
  return (
    <ListGroup>
      <ListGroupItem className={`font-weight-bold d-flex p-4`} tag={Row}>
              <Col xs={2} className="text-center">#</Col>
              <Col xs={8}>User</Col>
              <Col xs={2} className="text-center">Score</Col>
      </ListGroupItem>
      { leaders.map((leader, idx) => (
        <ListGroupItem key={leader.id} tag={Row} className="d-flex align-items-center p-4">
          <Col xs={2} className="text-center">
            { idx == 0 ? 
                <i className={`fas fa-trophy ${classes.gold}`} /> :
              idx == 1 ?
                <i className={`fas fa-trophy ${classes.silver}`} /> :
              idx == 2 ?
                <i className={`fas fa-trophy ${classes.bronze}`} /> :
              { idx }
            }
          </Col>
          <Col xs={8}>
            <Row className="d-flex align-items-center flex-nowrap pl-3">
              <img src={`https://www.gravatar.com/avatar/f9879d71855b5ff21e4963273a886bfc?d=retro&size=30`}
                    alt="hackshaw termninja profile"
                    className="rounded-circle mr-3 d-none d-md-block"
                    width="30"
                    height="30" />
                { leader.username ? 
                    <Link href="/u/[username]" as={`/u/${leader.username}`}>
                      <a className="text-dark text-truncate">
                        { leader.username }
                      </a>
                    </Link>
                  :
                  <span className="text-dark text-truncate">
                    anonymous
                  </span>
                }
            </Row>
          </Col>
          <Col xs={2} className="text-center">
            { leader.score }
          </Col>
        </ListGroupItem>
      ))}
    </ListGroup>
  )
}

export default Leaderboard;
