import * as root from './root';



const login = (username, password) => {
  return root.post('/auth', { username, password })
}

const logout = () => {
  return root.get('/auth/logout');
}

const getMe = async ctx => {
  const { me } = await root.get('/auth/me', ctx);
  if (!me) {
    throw new Error('Bad Token')
  }
  return me;
}

const getUser = async username => {
  return root.get(`/user/${username}`)
}

const listRounds = async (username, page=0) => {
  return root.get(`/user/${username}/rounds?page=${page}`)
}

export default {
  getMe,
  login,
  logout,
  getUser,
  listRounds
}
