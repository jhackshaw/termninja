import React from 'react';
import { Container } from 'reactstrap';
import Layout from '../components/Layout';
import Jumbo from '../components/Jumbo';
import GamesTable from '../components/GamesTable';
import api from '../api';



const Home = ({ games }) => {
  return (
    <Layout>
      <Jumbo>
        <h2 className="display-4">Termninja</h2>
        <p className="mb-1"><b>ter·mi·nal</b> <em>(adj)</em>: text-based interface for typing commands.</p>
        <p><b>nin·ja</b> <em>(noun)</em>: a person skilled in ninjutsu.</p>
      </Jumbo>
      <Container>
        <GamesTable games={games} />
      </Container>
    </Layout>
  )
}

Home.getInitialProps = async () => {
  const games = await api.game.listGames();
  return { games }
}

export default Home;
