import React from 'react';
import App, { Container } from 'next/app';
import UserContext from '../ctx/UserContext';
import nookies from 'nookies';
import api from '../api';


class MyApp extends App {
  constructor(props) {
    super(props)
    this.state = {
      user: null
    }
    this.loginUser = this.loginUser.bind(this);
    this.logoutUser = this.logoutUser.bind(this);
  }

  static async getInitialProps({ Component, ctx }) {
    let pageProps = {};

    if (Component.getInitialProps) {
      pageProps = await Component.getInitialProps(ctx);
    }

    if (!ctx.req) {
      // on the client
      return { pageProps }
    }

    // on the server
    const user = await this.getUser(ctx);

    return { pageProps, user };
  }

  static async getUser(ctx) {
    const { token } = nookies.get(ctx);
    if (!token) {
      return null
    }
    try {
      return await api.user.getMe(ctx);
    } catch (e) {
      nookies.destroy(ctx, 'token')
      return null
    }
  }

  componentDidMount() {
    this.setState({
      user: this.props.user
    })
  }

  async loginUser(username, password) { 
    const { access_token } = await api.user.login(
      username,
      password
    );
    nookies.set(undefined, 'token', access_token);
    await this.refreshUser();
  }
    
  async logoutUser() {
    nookies.destroy(undefined, 'token');
    this.setState({
      user: null
    })
  }
    
  async refreshUser() {
    const user = await MyApp.getUser();
    this.setState({ user })
  }

  render() {
    const { Component, pageProps } = this.props;
    const userCtx = {
      user: this.state.user,
      loginUser: this.loginUser,
      logoutUser: this.logoutUser
    }

    return (
      <UserContext.Provider value={userCtx}>
        <Component {...pageProps} />
      </UserContext.Provider>
    );
  }
}

export default MyApp;
