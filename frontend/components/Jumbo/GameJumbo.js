import React from 'react';
import { Row,
         Col } from 'reactstrap';
import Jumbo from '.';


export const GameJumbo = ({ server_name, description, slug }) => {

  return (
    <Jumbo>
      <Row className="align-items-center">
        <Col xs="12" sm="10" md="6">
          <h2 className="display-4">{ server_name }</h2>
          <small>{ description }</small>
        </Col>
        <Col className="d-none d-md-flex flex-row justify-content-center" md="6">
          <img className="rounded" width="250" height="141" src={`/static/${slug}.jpg`} />
        </Col>
      </Row>
  </Jumbo>
  )
}

