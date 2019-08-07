import * as root from './root';

const listGames = async () => {
  try {
    return root.get('/game');
  } catch (e) {
    console.log(e)
    return []
  }
}

const getGame = async gameSlug => {
  try {
    return root.get(`/game/${gameSlug}`)
  } catch(e) {
    console.log(e)
    return {}
  }
}

const getLeaderboard = async gameSlug => {
  return root.get(`/game/${gameSlug}/leaderboard`)
}

const listRounds = async (gameSlug, page=0) => {
  try {
    return root.get(`/game/${gameSlug}/round?page=${page}`)
  } catch (e) {
    console.log(e)
    return []
  }
}

export default {
  listGames,
  listRounds,
  getGame,
  getLeaderboard
}
