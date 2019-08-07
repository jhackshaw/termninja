import * as root from './root';



const login = (username, password) => {
  return root.post('/auth', { username, password })
}

const logout = () => {
  return root.get('/auth/logout');
}

const getUser = async (username, ctx) => {
  return root.get(`/user/${username}`, ctx)
}

const listRounds = async (username, page=0) => {
  return root.get(`/user/${username}/rounds?page=${page}`)
}

const refreshPlayToken = async () => {
  return root.post(`/user/refresh_play_token`)
}

export default {
  login,
  logout,
  getUser,
  listRounds,
  refreshPlayToken
}
