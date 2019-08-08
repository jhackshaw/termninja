import React from 'react';
import Link from 'next/link';
import { DropdownItem } from 'reactstrap';
import classes from './NavbarDropdown.css';


const ProfileItem = ({ user }) => {

  return (
    <Link href="/u/[username]" as={`/u/${user.username}`}>
      <a className={classes.noHover}>
        <DropdownItem className={`d-flex align-items-center ${classes.ddItem}`}>
          <img src={`https://www.gravatar.com/avatar/${user.gravHash}?d=retro&size=30`}
                alt="hackshaw termninja profile"
                className="rounded-circle mr-3"
                width="30"
                height="30" />
          <div className="d-flex flex-column py-3">
            <span>{ user.username }</span>
          </div>
        </DropdownItem>
      </a>
    </Link>
  )
}

export default ProfileItem;
