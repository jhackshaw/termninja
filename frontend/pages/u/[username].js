import React, { useState } from 'react';
import Router from 'next/router';
import nookies from 'nookies';
import { Container, Col, Row } from 'reactstrap';
import { UserJumbo } from '../../components/Jumbo';
import Layout from '../../components/Layout';
import RoundList from '../../components/RoundList';
import PageButtons from '../../components/PageButtons';
import PlayTokenDisplay from '../../components/PlayTokenDisplay';
import api from '../../api';


const User = ({ user, rounds, prev_page, next_page }) => {  
  return (
    <Layout>
      <UserJumbo {...user} />

      <Container>
        { user.play_token &&
          <Row className=" mb-3">
            <Col xs={12} lg={6}>
              <PlayTokenDisplay {...user} />
            </Col>
          </Row>
        }
        <RoundList rounds={rounds} />

        <PageButtons href='/u/[username]'
                     as={`/u/${user.username}`}
                     next_page={next_page}
                     prev_page={prev_page} />
      </Container>
    </Layout>
  )
}

User.getInitialProps = async (ctx, currentUser=null) => {
  const { res, query: { username, page=0 }} = ctx;
  console.log(ctx.query);

  const [result, user] = await Promise.all([
    api.user.listRounds(username, page),
    username == currentUser ?
      api.user.getMe(ctx) :
      api.user.getUser(username)
  ]).catch(() => {
    if (res) {
      nookies.destroy(ctx, 'token');
      res.writeHead(302, {
        Location: '/login'
      })
      res.end()
    } else {
      Router.push('/login')
    }
  })
  const { prev_page, rounds, next_page } = result;
  return { prev_page, rounds, next_page, user }
}


export default User;
