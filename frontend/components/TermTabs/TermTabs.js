import React from "react";
import { Nav } from "reactstrap";
import classes from "./TermTabs.css";

const TermTabs = ({ children }) => {
  return (
    <Nav
      className={`${classes.root} d-flex align-items-center justify-content-center mb-4`}
    >
      {children}
    </Nav>
  );
};

export default TermTabs;
