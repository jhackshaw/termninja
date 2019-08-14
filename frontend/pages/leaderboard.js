import React from 'react';
import { Container } from 'reactstrap';
import Layout from '../components/Layout';
import { LeaderboardJumbo } from '../components/Jumbo';
import { GlobalLeaderboardList } from '../components/RoundList';
import api from '../api';


const GlobalLeaderboard = ({ leaders }) => {

  return (
    <Layout>
      <LeaderboardJumbo />

      <Container>
        <GlobalLeaderboardList leaders={leaders} />
      </Container>
    </Layout>
  )
}


GlobalLeaderboard.getInitialProps = async ctx => {
  const leaders = await api.user.getLeaders();
  return { leaders }
}

export default GlobalLeaderboard;
