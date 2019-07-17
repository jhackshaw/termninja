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

export default {
  listGames,
  getGame
}
