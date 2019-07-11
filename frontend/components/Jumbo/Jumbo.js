import React from 'react';
import { Jumbotron, Row, Col } from 'reactstrap';
import classes from './Jumbo.css';


const Jumbo = ({ title, children }) => (
  <Jumbotron className={`p-3 p-lg-4 ${classes.root}`} fluid>
    <Row>
      <Col sm={{size:12}} md={{size:10, offset:2}} lg={{size:6, offset:3}} className="my-2 text-white text-left">
        <h2 className="display-4">{ title }</h2>
        { children }
      </Col>
    </Row>
  </Jumbotron>
)

export default Jumbo;
