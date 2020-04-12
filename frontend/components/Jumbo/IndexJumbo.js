import React from "react";
import Jumbo from "./Jumbo";

export const IndexJumbo = (props) => {
  return (
    <Jumbo>
      <h2 className="display-4">Termninja</h2>
      <p className="mb-1">
        <b>ter·mi·nal</b> <em>(n)</em>: text-based interface for typing
        commands.
      </p>
      <p>
        <b>nin·ja</b> <em>(n)</em>: a person skilled in ninjutsu.
      </p>
    </Jumbo>
  );
};
