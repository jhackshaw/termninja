import React from 'react';
import { Grid, Hidden } from '@material-ui/core';
import GameTile from '../src/GameTile';
import Layout from '../src/Layout';
import Jumbotron from '../src/Jumbotron';
import CssBaseline from '@material-ui/core/CssBaseline';

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
      <>
      <CssBaseline />
      <Layout>
        <Jumbotron />
          <Grid container justify="center" spacing={0}>

            <Grid item container direction="column" wrap="nowrap" xs={12} sm={10} md={8}>
              {games.map(game => (
                <GameTile {...game} key={game.name} />
              ))}  
            </Grid>

          </Grid>
      </Layout>
      </>
    )
  }
}

export default Home;