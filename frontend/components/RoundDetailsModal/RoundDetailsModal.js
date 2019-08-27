import React, { useState, useEffect } from 'react';
import { Modal,
         ModalBody } from 'reactstrap';
import api from '../../api';
import RoundModalHeader from './RoundModalHeader';
import classes from './RoundDetailsModal.css';


const emptyRound = {
  'server_name': '',
  'result_snapshot': '',
  'result_message': '',
  'user_username': '',
  'gravatar_hash': '',
  'score': 0,
}

const RoundDetailsModal = ({ roundId, onClose }) => {
  const [round, setRound] = useState(emptyRound);

  useEffect(() => {
    const updateRound = async () => {
      let round = emptyRound;
      if (roundId) {
        round = await api.round.getDetails(roundId);
      }
      setRound(round)
    }
    updateRound();
  }, [roundId])

  return (
    <Modal isOpen={Boolean(roundId)} className={classes.root}>
      <ModalBody>
        <RoundModalHeader { ...round } onClose={onClose} />
        <span className={`${classes.message} m-2`}>{ round.message }</span>
        { round.snapshot &&
          <pre className={`${classes.snapshot} py-3 pr-2 mt-3`} 
               dangerouslySetInnerHTML={{ __html: round.snapshot }} />
        }
      </ModalBody>

    </Modal>
  )
}

export default RoundDetailsModal;
