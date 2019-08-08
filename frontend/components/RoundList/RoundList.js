import React from 'react';
import moment from 'moment';
import Link from 'next/link';
import { ListGroup,
         ListGroupItem,
         Row,
         Col } from 'reactstrap';


const GamesList = ({ rounds, show_user=false, show_game=false }) => {

  return (
    <ListGroup>
      <ListGroupItem className={`font-weight-bold d-flex p-4`} tag={Row}>
        <Col xs={4} md={3} className="">{ show_user ? 'User' : 'Game' }</Col>
        <Col xs={5} md={6}>Played</Col>
        <Col xs={3} className="text-center">Score</Col>
      </ListGroupItem>
      { rounds.map(round => (
        <ListGroupItem key={round.id} className="d-flex align-items-center p-4" tag={Row}>
          <Col xs={4} md={3}>
            <Row className="d-flex align-items-center flex-nowrap pl-3">
              { show_user &&
                <>
                <div className="d-none d-md-block">
                  <img src={`https://www.gravatar.com/avatar/f9879d71855b5ff21e4963273a886bfc?d=retro&size=30`}
                      alt="hackshaw termninja profile"
                      className="rounded-circle mr-3"
                      width="30"
                      height="30" 
                      />
                </ div>
                  { round.username ? 
                      <Link href="/u/[username]" as={`/u/${round.username}`}>
                        <a className="text-dark text-truncate">
                          { round.username }
                        </a>
                      </Link>
                    :
                    <span className="text-dark text-truncate">
                      anonymous
                    </span>
                  }
                </>
              }
              
              { show_game &&
                round.server_name
              }
              
                
            </Row>
          </Col>
          <Col xs={5} md={6} className="text-truncate">
            { moment.unix(round.played_at).fromNow() }
          </Col>
          <Col xs={3} className="text-center">
            { round.score }
          </Col>
        </ListGroupItem>
      ))}
    </ListGroup>
  )
}

export default GamesList;
