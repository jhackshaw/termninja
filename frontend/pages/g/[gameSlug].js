import React, { useState } from 'react';
import Link from 'next/link';
import { Container } from 'reactstrap';
import { GameJumbo } from '../../components/Jumbo';
import Layout from '../../components/Layout';
import RoundList from '../../components/RoundList';
import PageButtons from '../../components/PageButtons';
import api from '../../api';


const Game = ({ game, rounds, next_page, prev_page }) => {  
  return (
    <Layout>
      <GameJumbo {...game} />

      <Container>      
        <RoundList rounds={rounds} />
        <PageButtons href='/g/[gameSlug]'
                     as={`/g/${game.slug}`}
                     next_page={next_page}
                     prev_page={prev_page} />
      </Container>
    </Layout>
  )
}

Game.getInitialProps = async ({req, query: { gameSlug, page=0 }}) => {
  const [result, game] = await Promise.all([
    api.game.listRounds(gameSlug, page),
    api.game.getGame(gameSlug)
  ])
  const { prev_page, rounds, next_page } = result;
  return { prev_page, rounds, next_page, game }
}


export default Game;
