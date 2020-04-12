import React from "react";
import { Container } from "reactstrap";
import Layout from "../../../components/Layout";
import { GameJumbo } from "../../../components/Jumbo";
import { RoundListForGameLeaderboard } from "../../../components/RoundList";
import TermTabs, { TermTabItem } from "../../../components/TermTabs";
import api from "../../../api";

const GameLeaderboard = ({ game, top_rounds }) => {
  return (
    <Layout>
      <GameJumbo {...game} />

      <Container>
        <TermTabs>
          <TermTabItem href="/g/[gameSlug]" as={`/g/${game.slug}`}>
            <i className="fas fa-clock" /> Recent
          </TermTabItem>
          <TermTabItem
            active
            href="/g/[gameSlug]/leaderboard"
            as={`/g/${game.slug}/leaderboard`}
          >
            <i className="fas fa-trophy" /> Leaderboard
          </TermTabItem>
        </TermTabs>

        <RoundListForGameLeaderboard top_rounds={top_rounds} />
      </Container>
    </Layout>
  );
};

GameLeaderboard.getInitialProps = async ({ query: { gameSlug } }) => {
  const [top_rounds, game] = await Promise.all([
    api.game.getLeaderboard(gameSlug),
    api.game.getGame(gameSlug),
  ]);
  return { top_rounds, game };
};

export default GameLeaderboard;
