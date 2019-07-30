import React from 'react';
import { FormGroup,
         Label,
         Col,
         Input,
         InputGroup,
         InputGroupAddon,
         Button,
         FormText } from 'reactstrap';
import moment from 'moment';


const PlayTokenDisplay = ({ play_token, play_token_expires_at }) => {

  return (
    <FormGroup row>
      <Label for="playToken" sm={12}>Play Token</Label>
      <Col sm={12}>
        <InputGroup>
          <Input value={play_token} disabled />
          <InputGroupAddon addonType="append">
            <Button><i className="fas fa-copy" /></Button>
          </InputGroupAddon>
        </InputGroup>
          <FormText color="muted">
            Expires { moment.unix(play_token_expires_at).toNow() }
          </FormText>
      </Col>
    </FormGroup>
  )
}

export default PlayTokenDisplay;
