import React, { useState } from 'react';
import { Container } from 'reactstrap';
import { GameJumbo } from '../../components/Jumbo';
import Layout from '../../components/Layout';
import api from '../../api';


const Game = ({ game, rounds }) => {  
  return (
    <Layout>
      <GameJumbo {...game} />

      <Container>      
        <RoundList rounds={rounds} />
      </Container>
    </Layout>
  )
}

Game.getInitialProps = async ({req, query: { gameSlug }}) => {
  const [rounds, game] = await Promise.all([
    api.game.listRounds(gameSlug),
    api.game.getGame(gameSlug)
  ])
  return { rounds, game }
}


export default Game;
