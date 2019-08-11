import React from 'react';
import { Row,
         Col } from 'reactstrap';
import Jumbo from '.';


export const LeaderboardJumbo = props => {

  return (
    <Jumbo>
      <Row className="align-items-center">
        <Col xs="12" sm="10" md="6">
          <h2 className="display-4">Leaderboard</h2>
          <small>Global combined score leaderboard</small>
        </Col>
      </Row>
  </Jumbo>
  )
}

