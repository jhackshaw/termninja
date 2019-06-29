import React from 'react';
import { Grid } from '@material-ui/core';
import GameTile from '../src/GameTile';
import Layout from '../src/Layout';
import Jumbotron from '../src/Jumbotron';

const games = [
  { name: "Subnet Racer", image: "subnet_racer.jpg", description: "How fast can you calculate basic subnets?" },
  { name: "Tic Tac Toe", image: "tic_tac_toe.jpg", description: "Play against a random player in tic-tac-toe, winner take all!" },
  { name: "Snake", image: "snake.jpg", description: "The classic game of snake!" }
]


class Home extends React.Component {
  static async getInitialProps({ req }) {
    return { games }
  }

  render() {
    const { games } = this.props; 
    return (
      <Layout>
        <Jumbotron>
          
        </Jumbotron>
        <div style={{ padding: 20 }}>
          <Grid container justify="center" alignItems="stretch" spacing={4}>
            {games.map(game => (
              <Grid key={game.name} item xs={12} md={2} lg={3}>
                <GameTile {...game} />
              </Grid>
            ))}
          </Grid>
        </div>
      </Layout>
    )
  }
}

export default Home;