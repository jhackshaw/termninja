import React, { useState } from 'react';
import Link from 'next/link';
import { ListGroup } from 'reactstrap';
import RoundListItem from './RoundListItem';
import RoundDetailsModal from '../RoundDetailsModal';


const RoundListForGame = ({ rounds }) => {

  const [displayedRound, setDisplayedRound] = useState(null);

  return (
    <>
    <ListGroup>
    { rounds.map(r => (
      <RoundListItem key={r.id}
                     onClick={
                       e => setDisplayedRound(r.id)
                     }
                     avatar={
                       r. gravatar_hash ?
                          <img src={`https://www.gravatar.com/avatar/${r.gravatar_hash}?d=retro&size=30`}
                                alt="hackshaw termninja profile"
                                className="rounded-circle mr-3"
                                width="30"
                                height="30" 
                                />
                          :
                          <div style={{ width: 30, height: 30 }}>
                            <i className="text-muted fas fa-2x fa-fw fa-user-circle" />
                          </div>
                     }
                     displayName={
                       r.username ? 
                        <span onClick={e => e.stopPropagation()}>
                          <Link href="/u/[username]" as={`/u/${r.username}`}>
                            <a className="text-dark text-truncate">
                              { r.username }
                            </a>
                          </Link>
                         </span>
                         :
                         <span className="text-dark text-truncate">
                           anonymous
                         </span>
                     }
                     { ...r }
                     />
    ))}
    </ListGroup>
    
    <RoundDetailsModal roundId={displayedRound}
                       onClose={() => setDisplayedRound(null)} />
    </>
  )
}

export default RoundListForGame;
