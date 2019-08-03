import React from 'react';
import Head from 'next/head';
import Termnav from '../Termnav/Termnav';
import css from './Layout.css';


const Layout = ({ children, title='termninja' }) => (
  <>
  <Head>
    <title>{ title }</title>\
    <link rel="stylesheet" 
          href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css"
          integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm"
          crossOrigin="anonymous" />
    <link rel="stylesheet"
          href="https://fonts.googleapis.com/css?family=Roboto+Mono&display=swap" />
    <link rel="stylesheet"
          href="https://use.fontawesome.com/releases/v5.6.3/css/all.css"
          integrity="sha384-UHRtZLI+pbxtHCWp1t77Bi1L4ZtiqrqD80Kn4Z8NTSRyMA2Fd33n5dQ8lWUE00s/"
          crossorigin="anonymous" />
  </Head>

  <Termnav />
  
  <div className={css.content}>
    { children }
  </div>
  </>
)

export default Layout;
