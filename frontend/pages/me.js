import React, { useState } from 'react';
import { Container } from 'reactstrap';
import { UserJumbo } from '../components/Jumbo';
import Layout from '../components/Layout';
import RoundList from '../components/RoundList';
import PlayTokenDisplay from '../components/PlayTokenDisplay';
import api from '../api';


const Me = ({ me, rounds }) => {  
  return (
    <Layout>
      <UserJumbo {...me} />


      <Container>      
        <PlayTokenDisplay {...me} />
        <RoundList rounds={rounds} />
      </Container>
    </Layout>
  )
}

Me.getInitialProps = async (ctx, { username }) => {
  const { query: { page=0 }} = ctx;

  const [rounds, me] = await Promise.all([
    api.user.listRounds(username, page),
    api.user.getMe(ctx)
  ])
  return { rounds, me }
}


export default Me;

