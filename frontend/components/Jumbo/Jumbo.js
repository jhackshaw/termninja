import React from 'react';
import { Jumbotron, Container } from 'reactstrap';
import classes from './Jumbo.css';


const Jumbo = ({ children }) => (
  <Jumbotron className={`p-3 p-lg-4 text-white ${classes.root}`} fluid>
    <Container>
      { children }
    </Container>
  </Jumbotron>
)

export default Jumbo;
