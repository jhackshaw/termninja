import React, { useState } from 'react';
import { Col,
         Row,
         ListGroup,
         ListGroupItem } from 'reactstrap';
import classes from './PlayTokenDisplay.css';
import moment from 'moment';
import api from '../../api';


const PlayTokenDisplay = ({ play_token, play_token_expires_at}) => {
  const [playToken, setPlayToken] = useState(play_token)
  const [playTokenExpiresAt, setPlayTokenExpiresAt] = useState(play_token_expires_at)

  const tokenExpiration = moment.unix(playTokenExpiresAt);
  const tokenExpired = tokenExpiration < moment();
    
  const onCopyClick = async e => {
    await navigator.clipboard.writeText(play_token);
  }

  const onRefreshClick = async e => {
    const { play_token, play_token_expires_at } = await api.user.refreshPlayToken()
    setPlayToken(play_token)
    setPlayTokenExpiresAt(play_token_expires_at)
  }
  
  return (
    <ListGroup className="mb-3">
      <ListGroupItem tag={Row} className="d-flex align-items-center p-4">
        <Col xs="12" lg="6" className="text-truncate text-muted">
          { playToken }
        </Col>
        <Col xs="12" lg="4" className="text-truncate">
          expire{ tokenExpired ? 'd' : 's' } { moment().to(tokenExpiration) }
        </Col>
        <Col xs="12" lg="2" className="my-2 my-lg-0">
          <span className={`px-2 ${classes.btn}`} onClick={onCopyClick}>
            <i className="fas fa-copy" />
          </span>
          <span className={`px-2 ${classes.btn}`} onClick={onRefreshClick}>
            <i className="fas fa-sync" />
          </span>
        </Col>
      </ListGroupItem>
    </ListGroup>
  )
}

export default PlayTokenDisplay;
