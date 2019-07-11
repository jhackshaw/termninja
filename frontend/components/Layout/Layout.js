import React from 'react';
import Head from 'next/head';
import Termnav from '../Termnav/Termnav';
import { Container } from 'reactstrap';
import css from './Layout.css';


const Layout = ({ children, title='termninja' }) => (
  <>
  <Head>
    <title>{ title }</title>
    <link rel="stylesheet" 
          href="https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css" 
          integrity="sha384-MCw98/SFnGE8fJT3GXwEOngsV7Zt27NXFoaoApmYm81iuXoPkFOJwJ8ERdknLPMO" 
          crossOrigin="anonymous" />
    <link href="https://fonts.googleapis.com/css?family=Roboto+Mono&display=swap" rel="stylesheet" />
    <script src="https://kit.fontawesome.com/8f17ca51d5.js"></script>
  </Head>
  <Termnav />
  <div className={css.content}>
    { children }
  </div>
  </>
)

export default Layout;
