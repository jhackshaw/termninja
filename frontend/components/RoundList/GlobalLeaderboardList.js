import React from 'react';
import Link from 'next/link';
import classNames from 'classnames';
import { ListGroup } from 'reactstrap';
import RoundListItem from './RoundListItem';
import classes from './RoundList.css';


const GlobalLeaderboardList = ({ leaders }) => {

  return (
    <ListGroup>
    { leaders.map((r, idx) => (
      <RoundListItem key={r.id}
                     avatar={
                        <div className={classes.textAvatar}>
                          { idx < 3 ?
                            <i className={classNames({
                              [classes.gold]: idx === 0,
                              [classes.silver]: idx === 1,
                              [classes.bronze]: idx === 2,
                              ['fas fa-trophy fa-2x fa-fw']: true
                            })} />
                            :
                            <span>{ idx + 1 }</span>
                          }
                        </div>
                     }
                     displayName={
                       r.username ? 
                         <Link href="/u/[username]" as={`/u/${r.username}`}>
                           <a className="text-dark text-truncate">
                             { r.username }
                           </a>
                         </Link>
                         :
                         <span className="text-dark text-truncate">
                           anonymous
                         </span>
                     }
                     score={ r.total_score }
                     />
    ))}
    </ListGroup>
  )
}

export default GlobalLeaderboardList;
