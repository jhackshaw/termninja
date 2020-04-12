import React from "react";
import { Row, Col } from "reactstrap";
import Jumbo from ".";

export const GameJumbo = ({ name, icon, description }) => {
  return (
    <Jumbo>
      <Row className="align-items-center">
        <Col xs="12" md="10">
          <h2 className="display-4">{name}</h2>
          <small>{description}</small>
        </Col>
        <Col xs="2" className="text-center d-none d-md-block">
          <i className={`fas fa-3x fa-${icon || "gamepad"}`} />
        </Col>
      </Row>
    </Jumbo>
  );
};
