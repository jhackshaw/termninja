import React from 'react';
import Link from 'next/link';
import { Navbar } from 'reactstrap';
import classes from "./Termnav.css"


const Termnav = props => (
  <Navbar className={classes.root} color="light" expand="md" light>
    <Link href="/">
      <a className={classes.brand}>Termninja</a>
    </Link>
  </Navbar>
)

export default Termnav;
