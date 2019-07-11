import React from 'react';
import { Table, Card } from 'reactstrap';
import classes from './GamesTable.css';


const isOnline = game => true;


const GamesTable = ({games=[]}) => (
  <Card>
  <Table responsive>
    <thead>
      <tr>
        <th>Online</th>
        <th>Game</th>
        <th>Port</th>
        <th>Last Played</th>
      </tr>
    </thead>
    <tbody>
      { games.map(game => (
        <tr key={game.id}>
          <td>
            <i className={`fas fa-circle ${isOnline(game) ? classes.online : classes.offline}`} />
          </td>
          <td>{ game.name }</td>
          <td>{ game.port }</td>
          <td>{ game.lastPlayed }</td>
        </tr>
      ))}
    </tbody>
  </Table>
  </Card>
)

export default GamesTable;
