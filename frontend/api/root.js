import fetch from 'isomorphic-unfetch';
import nookies from 'nookies';


const baseUrl = process.env.TERMNINJA_API_URL || "http://localhost:8080"


const authHeader = ctx => {
  const { token } = nookies.get(ctx);
  if (token) {
    return {
      'Authorization': `Bearer ${token}`
    }
  }
  return {}
}

const request = async (url, params) => {
  const res = await fetch(`${baseUrl}${url}`, params)
  if (res.ok) {
    return res.json()
  }

  let data;
  if (res.headers.get('Content-Type') == 'application/json') {
    data = await res.json();
  }
  throw new Error(data['message'] || 'Something went wrong.')
}

export const get = (url, ctx) => (
  request(url, {
    method: 'GET',
    credentials: 'include',
    headers: {
      ...authHeader(ctx),
      'Content-Type': 'application/json'
    }
  })
)

export const post = (url, data, ctx) => (
  request(url, {
    method: 'POST',
    credentials: 'include',
    headers: {
      ...authHeader(ctx),
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(data)
  })
)
