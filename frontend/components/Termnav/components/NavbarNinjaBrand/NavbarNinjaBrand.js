import React from "react";
import Link from "next/link";
import classes from "./NavbarNinjaBrand.css";

const NavbarNinjaBrand = (props) => {
  return (
    <Link href="/">
      <a className={`${classes.brand} pl-1 pl-lg-5`}>
        <i className="fas fa-user-ninja" /> Termninja
      </a>
    </Link>
  );
};

export default NavbarNinjaBrand;
