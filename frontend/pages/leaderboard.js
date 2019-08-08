import React from 'react';
import { Container } from 'reactstrap';
import { LeaderboardJumbo } from '../components/Jumbo';
import Layout from '../components/Layout';
import Leaderboard from '../components/Leaderboard';
import api from '../api';


const GlobalLeaderboard = ({ leaders }) => {

  return (
    <Layout>
      <LeaderboardJumbo />

      <Container>
        <Leaderboard leaders={leaders} />
      </Container>
    </Layout>
  )
}


GlobalLeaderboard.getInitialProps = async ctx => {
  const leaders = await api.user.getLeaders();
  return { leaders }
}

export default GlobalLeaderboard;
