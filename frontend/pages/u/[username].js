import React, { useContext, useState } from 'react';
import { Container } from 'reactstrap';
import { UserJumbo } from '../../components/Jumbo';
import Layout from '../../components/Layout';
import RoundList from '../../components/RoundList';
import PageButtons from '../../components/PageButtons';
import api from '../../api';
import UserContext from '../../ctx/UserContext';


const User = ({ user, rounds, prev_page, next_page }) => {  
  const { logout } = useContext(UserContext);
  const [localUser, setLocalUser] = useState(user);

  const onLogout = () => {
    setLocalUser(user => {
      const { play_token, play_token_expires_at, ...rest } = user;
      return rest;
    })
    logout()
  }

  return (
    <Layout>
      <UserJumbo {...localUser}
                 onLogout={onLogout} />

      <Container>
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
