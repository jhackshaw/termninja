import React from 'react';
import Head from 'next/head';
import Termnav from '../Termnav/Termnav';
import css from './Layout.css';


const Layout = ({ children, title='termninja' }) => (
  <>
  <Head>
    <title>{ title }</title>
    <link rel="stylesheet" 
          href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css"
          integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm"
          crossorigin="anonymous" />
    <link rel="stylesheet"
          href="https://fonts.googleapis.com/css?family=Roboto+Mono&display=swap" />
    <script src="https://kit.fontawesome.com/8f17ca51d5.js"></script>
  </Head>

  <Termnav />
  
  <div className={css.content}>
    { children }
  </div>
  </>
)

export default Layout;
