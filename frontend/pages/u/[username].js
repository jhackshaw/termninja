import React, { useState } from 'react';
import { Container } from 'reactstrap';
import { UserJumbo } from '../../components/Jumbo';
import Layout from '../../components/Layout';
import RoundList from '../../components/RoundList';
import api from '../../api';


const Game = ({ user, rounds }) => {  
  return (
    <Layout>
      <UserJumbo {...user} />

      <Container>      
        <RoundList rounds={rounds} />
      </Container>
    </Layout>
  )
}

Game.getInitialProps = async ({req, query: { username, page=0 }}) => {
  const [rounds, user] = await Promise.all([
    api.user.listRounds(username, page),
    api.user.getUser(username)
  ])
  return { rounds, user }
}


export default Game;
