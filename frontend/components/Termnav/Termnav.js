import React, { useState } from 'react';
import Link from 'next/link';
import { Navbar,
         Media,
         NavbarBrand,
         Dropdown,
         DropdownToggle,
         DropdownMenu,
         DropdownItem } from 'reactstrap';
import classes from "./Termnav.css"


const Termnav = props => {
  const [isOpen, setIsOpen] = useState(false)

  return (
    <Navbar className={classes.root} color="faded" expand="md" light>
      <NavbarBrand tag={Link} href="/">
        <a className={`${classes.brand} pl-1 pl-lg-5`}>
          <i className="fas fa-user-ninja" />
          {' '}Termninja
        </a>
      </NavbarBrand>

      <Dropdown isOpen={isOpen} 
                toggle={() => setIsOpen(!isOpen)}
                className={`${classes.username} ml-auto pr-1 pr-lg-5 text-muted`}>
        <DropdownToggle tag="span" caret>
          Hackshaw
        </DropdownToggle>
        <DropdownMenu right>
          <DropdownItem>
            <div className="">
              <img src="https://www.gravatar.com/avatar/size=30&748afbc47ee5ae1f36dcd4f6a6946076?d=retro"
                   alt="hackshaw termninja profile"
                   className="rounded-circle"
                   width="30"
                   height="30" />
              <span className="">Hackshaw</span>
            </div>
          </DropdownItem>
        </DropdownMenu>
      </Dropdown>
    </Navbar>
  )
}

export default Termnav;
