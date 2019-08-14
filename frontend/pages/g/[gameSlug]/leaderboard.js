import React from 'react';
import { Container } from 'reactstrap';
import { GameJumbo } from '../../../components/Jumbo';
import { RoundListForGameLeaderboard } from '../../../components/RoundList';
import Layout from '../../../components/Layout';
import TermTabs, { TermTabItem } from '../../../components/TermTabs';
import api from '../../../api';


const GameLeaderboard = ({ game, top_rounds }) => {  
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

        <RoundListForGameLeaderboard top_rounds={top_rounds} />
      </Container>
    </Layout>
  )
}

GameLeaderboard.getInitialProps = async ({query: { gameSlug }}) => {
  const [top_rounds, game] = await Promise.all([
    api.game.getLeaderboard(gameSlug),
    api.game.getGame(gameSlug)
  ])
  return { top_rounds, game }
}


export default GameLeaderboard;
