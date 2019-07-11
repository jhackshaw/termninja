import React from 'react';
import { Jumbotron, Container } from 'reactstrap';
import classes from './Jumbo.css';


const Jumbo = ({ title, children }) => (
  <Jumbotron className={`p-3 p-lg-4 text-white ${classes.root}`} fluid>
    <Container>
      <h2 className="display-4">{ title }</h2>
          { children }
    </Container>
  </Jumbotron>
)

export default Jumbo;
