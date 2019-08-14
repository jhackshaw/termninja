import React from 'react';
import { ListGroupItem, Row, Col } from 'reactstrap';
import moment from 'moment';
import classes from './RoundList.css';


const RoundListItem = ({ id, avatar, displayName, played_at, score, onClick }) => {

  return (
    <ListGroupItem className={`d-flex align-items-center p-4 ${Boolean(onClick) && classes.clickable}`}
                   onClick={onClick}>
      <Col xs={1} className="pl-0 pl-md-2 pl-lg-4">
        { avatar }
      </Col>
      <Col xs={9}>
        <Row className="d-flex align-items-center pl-3">
          <Col xs={12} md={6}>
            { displayName }
          </Col>
          { played_at &&
            <Col xs={12} md={6}>
              { moment.unix(played_at).fromNow() }
            </Col>
          }
        </Row>
      </Col>
      <Col xs={2} className="text-center">
        { score }
      </Col>
    </ListGroupItem>
  )
}

export default RoundListItem;
