import fetch from "isomorphic-unfetch";

// call a different endpoint based on whether this is
// being rendered server side or client side
let baseUrl = process.env.TERMNINJA_CLIENT_API_URL;
if (typeof window === "undefined") {
  baseUrl = process.env.TERMNINJA_SERVER_API_URL;
}

const request = async (url, params) => {
  const res = await fetch(`${baseUrl}${url}`, params);
  if (res.ok) {
    return res.json();
  }

  let data = {};
  if (res.headers.get("Content-Type") === "application/json") {
    data = await res.json();
  }

  const err = new Error((data && data["message"]) || "Something went wrong");
  err.status = res.status;
  throw err;
};

export const get = (url) =>
  request(url, {
    method: "GET",
  });

export const post = (url, data, opts = {}) =>
  request(url, {
    method: "POST",
    body: JSON.stringify(data),
  });
