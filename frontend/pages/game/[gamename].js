import React from 'react';
import { useRouter } from 'next/router';
import { Col, Row } from 'reactstrap';
import Layout from '../../components/Layout';
import Jumbo from '../../components/Jumbo';


const defaultGame = {
  description: 'Subnetting in your head - on a time crunch',
  id: 1,
  port:3000
}

const Game = ({ name, id, port, description }) => {
  return (
    <Layout>
      <Jumbo>
        <Row className="align-items-center">
          <Col xs="12" sm="10" md="6">
            <h2 className="display-4">{ name }</h2>
            <p className="mb-1">{ description }</p>
          </Col>
          <Col className="d-none d-md-flex flex-row justify-content-center" md="6">
            <img className="rounded" width="250" height="141" src={`/static/${id}.jpg`} />
          </Col>
        </Row>
      </Jumbo>
    </Layout>
  )
}

Game.getInitialProps = ({req, query: { gamename }}) => {
  // const game = await api.getGame(gamename)
  return { ...defaultGame, name: gamename }
}


export default Game;
