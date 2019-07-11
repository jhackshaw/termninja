import React from 'react';
import { Container } from 'reactstrap'
import Layout from '../components/Layout';
import Jumbo from '../components/Jumbo';
import GamesTable from '../components/GamesTable';


const games_data = [
  { id: 1, lastPlayed: '25m ago', name: 'Subnet Racer', port: 3001 },
  { id: 2, lastPlayed: '1day ago', name: 'Snake', port: 3002 },
  { id: 3, lastPlayed: '2m ago', name: 'Tic-Tac-Toe', port: 3003 }
]


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

Home.getInitialProps = () => {
  return { games: games_data }
}

export default Home;
