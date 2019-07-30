import React from 'react';
import Router from 'next/router';
import nookies from 'nookies';


const Logout = props => {

  return (
    <span>Redirecting...</span>
  )
}


Logout.getInitialProps = ctx => {
  if (!ctx.res) {
    Router.push('/')
  }
  nookies.destroy(ctx, 'token');
  ctx.res.writeHead(302, {
    Location: '/'
  })
  ctx.res.end()
}

export default Logout;

