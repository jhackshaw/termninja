import * as root from "./root";

const getUser = async (username) => {
  return root.get(`/user/${username}`);
};

const getLeaders = async () => {
  return root.get("/user");
};

const listRounds = async (username, page = 0) => {
  return root.get(`/user/${username}/rounds?page=${page}`);
};

export default {
  getUser,
  getLeaders,
  listRounds,
};
