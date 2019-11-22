import React, { useState } from 'react';
import Link from 'next/link';
import { NavbarToggler,
         Collapse,
         Nav,
         NavItem,
         NavLink } from 'reactstrap';
import classes from './NavbarCollapse.css';


const NavbarUserDropdown = props => {
  const [isOpen, setIsOpen] = useState(false);


  const toggle = e => {
    setIsOpen(isOpen => !isOpen);
  }

  return (
    <>
    <NavbarToggler onClick={toggle} />
    <Collapse isOpen={isOpen} className={classes.root} navbar>
      <Nav className="ml-auto align-items-start align-items-sm-center" navbar>
        <NavItem className="ml-1 ml-lg-2">
          <Link href="/about" passHref>
            <NavLink className={classes.link}>
              <i className={`fas fa-lg fa-info-circle ${classes.linkicon}`} />
              <span className="d-inline-block d-sm-none ml-2">About</span>  
            </NavLink>  
          </Link>
        </NavItem>

        <NavItem className="ml-1 ml-lg-2">
          <Link href="/leaderboard" passHref>
            <NavLink className={classes.link}>
              <i className={`fas fa-lg fa-trophy ${classes.linkicon}`} />
              <span className="d-inline-block d-sm-none ml-2">Leaderboard</span>
            </NavLink>  
          </Link>
        </NavItem>

        <NavItem className="ml-1 ml-lg-2">
          <NavLink href="https://github.com/jhackshaw/termninja" className={classes.link}>
            <i className={`fab fa-lg fa-github ${classes.linkicon}`} />
            <span className="d-inline-block d-sm-none ml-2">Contribute</span>
          </NavLink> 
        </NavItem>


      </Nav>
    </Collapse>
    </>
  )
}

export default NavbarUserDropdown;
