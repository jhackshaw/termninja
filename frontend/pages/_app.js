import React from 'react';
import App from 'next/app';
import UserContext from '../ctx/UserContext';
import nookies from 'nookies';
import jwtDecode from 'jwt-decode';
import api from '../api';


class MyApp extends App {
  constructor(props) {
    super(props)
    this.state = {
      user: null
    }
    this.loginUser = this.loginUser.bind(this)
    this.logoutUser = this.logoutUser.bind(this)
  }

  static async getInitialProps({ Component, ctx }) {
    let pageProps = {};
    let currentUser = null;

    if (ctx.req) {
      const { token } = nookies.get(ctx);
      if (token) {
        currentUser = jwtDecode(token);
      }
    }

    if (Component.getInitialProps) {
      pageProps = await Component.getInitialProps(ctx, currentUser);
    }

    return { pageProps, currentUser };
  }

  async logoutUser() {
    await api.user.logout();
    this.setState({ currentUser: null })
  }

  async loginUser(username, password) {
    const { access_token } = await api.user.login(username, password);
    if (access_token) {
      this.setState({ currentUser: jwtDecode(access_token) })
    }
  }

  componentDidMount() {
    this.setState({
      currentUser: this.props.currentUser
    })
  }

  render() {
    const { Component, pageProps } = this.props;
    const userCtx = {
      user: this.state.currentUser,
      logout: this.logoutUser,
      login: this.loginUser
    }

    return (
      <UserContext.Provider value={userCtx}>
        <Component {...pageProps} />
      </UserContext.Provider>
    );
  }
}

export default MyApp;
