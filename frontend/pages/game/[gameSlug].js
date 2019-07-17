import React, { useState } from 'react';
import { Container } from 'reactstrap';
import Layout from '../../components/Layout';
import GameJumbo from '../../components/GameJumbo';
import api from '../../api';


const Game = ({ game }) => {  
  return (
    <Layout>
      <GameJumbo {...game} />

      <Container>      
      </Container>
    </Layout>
  )
}

Game.getInitialProps = async ({req, query: { gameSlug }}) => {
  const game = await api.game.getGame(gameSlug);
  return { game }
}


export default Game;
