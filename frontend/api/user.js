import * as root from './root';



const login = (username, password) => {
  return root.post('/auth', { username, password })
}

const getMe = async ctx => {
  const { me } = await root.get('/auth/me', ctx);
  if (!me) {
    throw new Error('Bad Token')
  }
  return me;
}

export default {
  getMe,
  login
}
