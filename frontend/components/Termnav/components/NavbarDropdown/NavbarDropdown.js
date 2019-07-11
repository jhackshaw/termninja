import React, { useState } from 'react';
import Link from 'next/link';
import { DropdownMenu,
         DropdownItem,
         Dropdown,
         DropdownToggle } from 'reactstrap';
import classes from './NavbarDropdown.css';


const NavbarDropdown = ({ user }) => {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <Dropdown isOpen={isOpen} 
              toggle={() => setIsOpen(!isOpen)}
              className={`${classes.username} ml-auto pr-1 pr-lg-5 text-muted`}>
      <DropdownToggle tag="span" caret>
        { user.username }
      </DropdownToggle>

      <DropdownMenu className={classes.menu} right>

        <Link href="/me">
          <DropdownItem className={`d-flex align-items-center ${classes.ddItem}`}>
            <img src={`https://www.gravatar.com/avatar/${user.gravHash}?d=retro&size=30`}
                  alt="hackshaw termninja profile"
                  className="rounded-circle mr-3"
                  width="30"
                  height="30" />
            <div className="d-flex flex-column">
              <span>{ user.username }</span>
              <small>Ninja Score: { user.score }</small>
            </div>
          </DropdownItem>
        </Link>

        <DropdownItem divider />


        <DropdownItem className={classes.ddItem}>
          <Link href="/leaderboard">
            <a className="text-muted">
              <i className="fas fa-trophy" />{' '}
              Leaderboard
            </a>
          </Link>
        </DropdownItem>

        <DropdownItem className={classes.ddItem}>
          <Link href="/about">
            <a className="text-muted">
              <i className="fas fa-info-circle" />{' '}
              About
            </a>
          </Link>
        </DropdownItem>


        <DropdownItem className={classes.ddItem}>
          <Link href="/about">
            <a className="text-muted">
              <i className="fab fa-github" />{' '}
              Contribute
            </a>
          </Link>
        </DropdownItem>


      </DropdownMenu>
    </Dropdown>
  )
}

export default NavbarDropdown;
