import React from 'react';
import { Container } from 'reactstrap';
import { GameJumbo } from '../../components/Jumbo';
import Layout from '../../components/Layout';
import RoundList from '../../components/RoundList';
import PageButtons from '../../components/PageButtons';
import TermTabs, { TermTabItem } from '../../components/TermTabs';
import api from '../../api';


const Game = ({ game, rounds, next_page, prev_page }) => {  
  
  return (
    <Layout>
      <GameJumbo {...game} />

      <Container>
        <TermTabs>
          <TermTabItem active href="/g/[gameSlug]" as={`/g/${game.slug}`}>
            Recent
          </TermTabItem>
          <TermTabItem href="/g/[gameSlug]/leaderboard" as={`/g/${game.slug}/leaderboard`}>
            Leaderboard
          </TermTabItem>
        </TermTabs>

        <RoundList rounds={rounds}
                   show_user />
        <PageButtons href='/g/[gameSlug]'
                     as={`/g/${game.slug}`}
                     next_page={next_page}
                     prev_page={prev_page} />
      </Container>
    </Layout>
  )
}

Game.getInitialProps = async ({query: { gameSlug, page=0 }}) => {
  const [result, game] = await Promise.all([
    api.game.listRounds(gameSlug, page),
    api.game.getGame(gameSlug)
  ])
  return { ...result, game }
}


export default Game;
