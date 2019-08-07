import React, { useState } from 'react';
import Router from 'next/router';
import nookies from 'nookies';
import { Container, Col, Row } from 'reactstrap';
import { UserJumbo } from '../../components/Jumbo';
import Layout from '../../components/Layout';
import RoundList from '../../components/RoundList';
import PageButtons from '../../components/PageButtons';
import PlayTokenDisplay from '../../components/PlayTokenDisplay';
import SectionHeader from '../../components/SectionHeader';
import api from '../../api';


const User = ({ user, rounds, prev_page, next_page }) => {  
  return (
    <Layout>
      <UserJumbo {...user} />

      <Container>
        { user.play_token &&
          <>
          <SectionHeader title="play token" />
          <PlayTokenDisplay {...user} />
          </>
        }

        <SectionHeader title="recently played" />
        <RoundList rounds={rounds}
                   show_game />

        <PageButtons href='/u/[username]'
                     as={`/u/${user.username}`}
                     next_page={next_page}
                     prev_page={prev_page} />
      </Container>
    </Layout>
  )
}

User.getInitialProps = async ctx => {
  const { query: { username, page=0 }} = ctx;

  const [result, user] = await Promise.all([
    api.user.listRounds(username, page),
    api.user.getUser(username, ctx)
  ])
  return { ...result, user }
}


export default User;
