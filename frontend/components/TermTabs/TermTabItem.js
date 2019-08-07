import React from 'react';
import classNames from 'classnames';
import { NavLink } from 'reactstrap';
import classes from './TermTabs.css';
import Link from 'next/link';


const TermTabItem = ({ active, children, ...rest }) => {

  return (
    <Link { ...rest }>
      <a className={classNames({ 
        [classes.active]: active,
        [classes.link]: true,
        ['px-4']: true,
        ['py-2']: true
      })}>
        { children }
      </a>
    </Link>
  )
}

export default TermTabItem;
