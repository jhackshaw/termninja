import React from 'react';
import { Navbar } from 'reactstrap';
import NavbarNinjaBrand from './components/NavbarNinjaBrand';
import NavbarDropdown from './components/NavbarDropdown';



const Termnav = props => {

  return (
    <Navbar color="faded" expand="md" light>
      <NavbarNinjaBrand />
      <NavbarDropdown />
    </Navbar>
  )
}

export default Termnav;
