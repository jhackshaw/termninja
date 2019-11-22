import fetch from 'isomorphic-unfetch';


const baseUrl = process.env.TERMNINJA_API_URL || "https://play.term.ninja"


const request = async (url, params) => {

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

export const get = (url) => (
  request(url, {
    method: 'GET'
  })
)

export const post = (url, data, opts={}) => (
  request(url, {
    method: 'POST',
    body: JSON.stringify(data)
  })
)
