import React from 'react';
import { Navbar } from 'reactstrap';
import NavbarNinjaBrand from './components/NavbarNinjaBrand';
import NavbarCollapse from './components/NavbarCollapse';



const Termnav = props => {

  return (
    <Navbar color="faded" expand="sm" light>
      <NavbarNinjaBrand />
      <NavbarCollapse />
    </Navbar>
  )
}

export default Termnav;
