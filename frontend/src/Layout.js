import React from 'react';
import { Container } from '@material-ui/core';
import Navbar from './Navbar';


const Layout = ({ children }) => {

  return (
    <>
    <Navbar />
    { children }
    </>
  )
}

export default Layout
