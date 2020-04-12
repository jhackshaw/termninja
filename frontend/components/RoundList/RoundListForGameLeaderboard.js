import React, { useState } from "react";
import Link from "next/link";
import classNames from "classnames";
import { ListGroup } from "reactstrap";
import RoundDetailsModal from "../RoundDetailsModal";
import RoundListItem from "./RoundListItem";
import classes from "./RoundList.css";

const RoundListForGameLeaderboard = ({ top_rounds }) => {
  const [displayedRound, setDisplayedRound] = useState(null);

  return (
    <>
      <ListGroup>
        {top_rounds.map((r, idx) => (
          <RoundListItem
            key={r.id}
            onClick={(e) => setDisplayedRound(r.id)}
            avatar={
              <div className={classes.textAvatar}>
                {idx < 3 ? (
                  <i
                    className={classNames({
                      [classes.gold]: idx === 0,
                      [classes.silver]: idx === 1,
                      [classes.bronze]: idx === 2,
                      ["fas fa-trophy fa-2x fa-fw"]: true,
                    })}
                  />
                ) : (
                  <div className="text-center">{idx + 1}</div>
                )}
              </div>
            }
            displayName={
              r.username ? (
                <Link href="/u/[username]" as={`/u/${r.username}`}>
                  <a className="text-dark text-truncate">{r.username}</a>
                </Link>
              ) : (
                <span className="text-dark text-truncate">anonymous</span>
              )
            }
            {...r}
          />
        ))}
      </ListGroup>

      <RoundDetailsModal
        roundId={displayedRound}
        onClose={() => setDisplayedRound(null)}
      />
    </>
  );
};

export default RoundListForGameLeaderboard;
