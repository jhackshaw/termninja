import React from 'react';
import { Row,
         Col,
         Button } from 'reactstrap';
import Jumbo from '.';
import classes from './Jumbo.css';


export const UserJumbo = ({ username, score, play_token, onLogout }) => {

  return (
    <Jumbo>
      <Row className="align-items-center">
        <Col xs="12" sm="3" lg="2" className="text-center p-4">
          <img src={`https://www.gravatar.com/avatar/f9879d71855b5ff21e4963273a886bfc?d=retro&size=120`}
                      alt="hackshaw termninja profile"
                      className="rounded-circle mr-3 img-fluid" />
        </Col>
        <Col xs="12" sm="9" lg="10" className="text-center text-sm-left">
          <h2 className="display-4">{ username }</h2>
          <p>Ninja Score: { score }</p> 
          { play_token &&
            <Button outline size="sm" className={`${classes.logoutBtn}`} onClick={onLogout}>
              logout
            </Button>
          }
        </Col>
      </Row>
  </Jumbo>
  )
}

