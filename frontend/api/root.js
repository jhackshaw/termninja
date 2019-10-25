import fetch from 'isomorphic-unfetch';
import nookies from 'nookies';


const baseUrl = process.env.TERMNINJA_API_URL || "https://play.term.ninja"


const authHeaders = ctx => {
  /*
    These headers will cause a preflight OPTIONS
    request due to api hosted on separate domain.
    Only send them when necessary
      e.g. authenticated requests
  */
  const { token } = nookies.get(ctx);
  if (token) {
    return {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json',
      'Accept': 'application/json'
    }
  }
  return {}
}

const request = async (url, params, opts) => {
  const { auth, ctx } = opts;
  if (auth) {
    params.headers = {
      ...params.headers || {},
      ...authHeaders(ctx)
    }
    params.credentials = 'include'
  }

  const res = await fetch(`${baseUrl}${url}`, params)
  if (res.ok) {
    return res.json()
  }

  let data = {};
  if (res.headers.get('Content-Type') === 'application/json') {
    data = await res.json();
  }

  const err = new Error(data && data['message'] || 'Something went wrong');
  err.status = res.status;
  throw err;
}

export const get = (url, opts={}) => (
  request(url, {
    method: 'GET'
  },
  opts)
)

export const post = (url, data, opts={}) => (
  request(url, {
    method: 'POST',
    body: JSON.stringify(data)
  },
  opts)
)
