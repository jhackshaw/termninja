import React from 'react';
import App from 'next/app';
import UserContext from '../ctx/UserContext';
import nookies from 'nookies';
import jwtDecode from 'jwt-decode';


class MyApp extends App {
  constructor(props) {
    super(props)
    this.state = {
      user: null
    }
  }

  static async getInitialProps({ Component, ctx }) {
    let pageProps = {};
    let user = null

    if (ctx.req) {
      // on the server, decode jwt from cookie
      const { token } = nookies.get(ctx);
      if (token) {
        user = jwtDecode(token);
      }
    }

    if (Component.getInitialProps) {
      pageProps = await Component.getInitialProps(ctx, user);
    }

    return { pageProps, user };
  }

  componentDidMount() {
    this.setState({
      user: this.props.user
    })
  }

  render() {
    const { Component, pageProps } = this.props;
    const userCtx = {
      user: this.state.user
    }

    return (
      <UserContext.Provider value={userCtx}>
        <Component {...pageProps} />
      </UserContext.Provider>
    );
  }
}

export default MyApp;
