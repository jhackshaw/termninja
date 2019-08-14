import React, { useState } from 'react';
import Link from 'next/link';
import { ListGroup } from 'reactstrap';
import RoundDetailsModal from '../RoundDetailsModal';
import RoundListItem from './RoundListItem';


const RoundListForUser = ({ rounds }) => {
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
                        <div style={{ width: 30, height: 30 }}>
                          <i className={`fas fa-2x fa-fw fa-${r.game_icon || 'dragon'}`} />
                        </div>
                     }
                     displayName={
                        <span onClick={e => e.stopPropagation()}>
                          <Link href="/g/[gameSlug]" as={`/g/${r.slug}`}>
                            <a className="text-dark text-truncate">
                              { r.name }
                            </a>
                          </Link>
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

export default RoundListForUser;
