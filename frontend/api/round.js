import * as root from "./root";

const getDetails = async (roundId) => root.get(`/round/${roundId}`);

export default {
  getDetails,
};
