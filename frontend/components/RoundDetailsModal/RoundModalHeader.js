import React from "react";
import moment from "moment";
import Link from "next/link";
import { Row, Col } from "reactstrap";

const RoundModalHeader = ({ username, gravatar_hash, played_at, onClose }) => {
  return (
    <div className="d-flex w-auto align-items-center p-3">
      <Col xs={2} className="pl-2">
        {gravatar_hash ? (
          <img
            src={`https://www.gravatar.com/avatar/${gravatar_hash}?d=retro&size=30`}
            alt="hackshaw termninja profile"
            className="rounded-circle mr-3"
            width="30"
            height="30"
          />
        ) : (
          <div style={{ width: 30, height: 30 }}>
            <i className="text-muted fas fa-2x fa-fw fa-user-circle" />
          </div>
        )}
      </Col>
      <Col xs={8}>
        <Row>
          {username ? (
            <Link href="/u/[username]" as={`/u/${username}`}>
              <a className="text-dark text-truncate">{username}</a>
            </Link>
          ) : (
            <span className="text-dark text-truncate">anonymous</span>
          )}
        </Row>
        <Row>{played_at && moment.unix(played_at).fromNow()}</Row>
      </Col>
      <Col xs={2} className="pr-2">
        <div className="btn" onClick={onClose}>
          <i className="fas fa-times fa-lg" />
        </div>
      </Col>
    </div>
  );
};

export default RoundModalHeader;
