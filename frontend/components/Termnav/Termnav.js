import React, { useState } from 'react';
import { Navbar } from 'reactstrap';
import NavbarNinjaBrand from './components/NavbarNinjaBrand';
import NavbarDropdown from './components/NavbarDropdown';


const defaultUser = {
  username: 'hackshaw',
  score: 23413,
  gravHash: 'ac1990a4972f59f54d7917f8ba3ce7a9'
}

const Termnav = ({ user=defaultUser }) => {
  const [isOpen, setIsOpen] = useState(false)

  return (
    <Navbar color="faded" expand="md" light>
      <NavbarNinjaBrand />
      <NavbarDropdown user={user} />
    </Navbar>
  )
}

export default Termnav;
