import React from 'react';
import { Container } from 'reactstrap';
import Layout from '../components/Layout';
import { IndexJumbo } from '../components/Jumbo';
import GamesList from '../components/GamesList/GamesList';
import api from '../api';



const Home = ({ games }) => {
  return (
    <Layout>
      <IndexJumbo />
      <Container>
        <GamesList games={games} />
      </Container>
    </Layout>
  )
}

Home.getInitialProps = async () => {
  const games = await api.game.listGames();
  return { games }
}

export default Home;
