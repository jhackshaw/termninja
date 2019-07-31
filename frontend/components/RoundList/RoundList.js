import React from 'react';
import moment from 'moment';
import Link from 'next/link';
import { ListGroup,
         ListGroupItem,
         Row,
         Col } from 'reactstrap';
import classes from './RoundList.css';


const GamesList = ({ rounds }) => {

  return (
    <ListGroup>
      {rounds.map(round => (
        <ListGroupItem key={round.id} className={classes.item} tag={Row}>
          <Col xs={5} lg={3} xl={2}>
            <Row className="d-flex align-items-center flex-nowrap">
              <img src={`https://www.gravatar.com/avatar/f9879d71855b5ff21e4963273a886bfc?d=retro&size=30`}
                    alt="hackshaw termninja profile"
                    className="rounded-circle mr-3"
                    width="30"
                    height="30" />
                { round.user_username ? 
                    <Link href="/u/[username]" as={`/u/${round.user_username}`}>
                      <a className="text-dark text-truncate">
                        { round.user_username || 'anonymous' }
                      </a>
                    </Link>
                  :
                  <span className="text-dark text-truncate">
                    anonymous
                  </span>
                }
                
            </Row>
          </Col>
          <Col xs={5} lg={3} xl={2} className="text-truncate">
            { moment.unix(round.played_at).fromNow() }
          </Col>
          <Col xs={2} lg={1} xl={2} className="text-center">
            <span className="text-secondary">+</span>{ round.score }
          </Col>
          <Col xs={12} lg={5} xl={6} className="text-secondary text-truncate pt-4 pt-lg-0 pl-0 pl-lg-1">
            <span>[{ round.server_name }]</span> { round.result_message }
          </Col>
        </ListGroupItem>
      ))}
    </ListGroup>
  )
}

export default GamesList;
