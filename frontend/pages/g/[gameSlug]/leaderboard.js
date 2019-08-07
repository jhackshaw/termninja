import React from 'react';
import { Container } from 'reactstrap';
import { GameJumbo } from '../../../components/Jumbo';
import Layout from '../../../components/Layout';
import Leaderboard from '../../../components/Leaderboard';
import PageButtons from '../../../components/PageButtons';
import TermTabs, { TermTabItem } from '../../../components/TermTabs';
import api from '../../../api';


const GameLeaderboard = ({ game, leaderboard, next_page, prev_page }) => {  
  return (
    <Layout>
      <GameJumbo {...game} />

      <Container>
        <TermTabs>
          <TermTabItem href="/g/[gameSlug]" as={`/g/${game.slug}`}>
            Recent
          </TermTabItem>
          <TermTabItem active href="/g/[gameSlug]/leaderboard" as={`/g/${game.slug}/leaderboard`}>
            Leaderboard
          </TermTabItem>
        </TermTabs>

        <Leaderboard leaders={leaderboard} />
      </Container>
    </Layout>
  )
}

GameLeaderboard.getInitialProps = async ({query: { gameSlug }}) => {
  const [leaderboard, game] = await Promise.all([
    api.game.getLeaderboard(gameSlug),
    api.game.getGame(gameSlug)
  ])
  return { leaderboard, game }
}


export default GameLeaderboard;
