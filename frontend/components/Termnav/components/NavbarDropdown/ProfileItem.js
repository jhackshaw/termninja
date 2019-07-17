import React from 'react';
import Link from 'next/link';
import { DropdownItem } from 'reactstrap';
import classes from './NavbarDropdown.css';


const ProfileItem = ({ user }) => {

  return (
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
  )
}

export default ProfileItem;
