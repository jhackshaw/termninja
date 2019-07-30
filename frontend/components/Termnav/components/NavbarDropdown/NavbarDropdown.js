import React, { useState, useContext } from 'react';
import Link from 'next/link';
import { DropdownMenu,
         DropdownItem,
         Dropdown,
         DropdownToggle } from 'reactstrap';
import UserContext from '../../../../ctx/UserContext';
import ProfileItem from './ProfileItem';
import AuthLinks from './AuthLinks';
import classes from './NavbarDropdown.css';


const NavbarUserDropdown = props => {
  const { user, logoutUser} = useContext(UserContext)
  const [isOpen, setIsOpen] = useState(false);

  return (
    <Dropdown isOpen={isOpen}
              toggle={() => setIsOpen(!isOpen)}
              className={`${classes.root} ml-auto pr-1 pr-lg-5 text-muted`}>
      <DropdownToggle tag="span" caret className={classes.toggle}>
        { user ? user.username : <i className="fas fa-cog"></i> }
      </DropdownToggle>

      <DropdownMenu className={classes.menu} right>

        { user ? 
            <ProfileItem user={user} /> :
            <AuthLinks />
        }

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
          <a href="https://github.com/jhackshaw/termninja" className="text-muted">
            <i className="fab fa-github" />{' '}
            Contribute
          </a>
        </DropdownItem>

        { user &&
          <DropdownItem className={`${classes.ddItem} text-muted`}>
            <a href="/logout">
              <i className="fas fa-sign-out-alt" />{' '}
              Logout
            </a>
          </DropdownItem>
        }


      </DropdownMenu>
    </Dropdown>
  )
}

export default NavbarUserDropdown;
