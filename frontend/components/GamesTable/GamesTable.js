import React from 'react';
import { Table, Card } from 'reactstrap';
import css from './GamesTable.css';


const isOnline = game => true;


const GamesTable = ({games=[]}) => (
  <Card>
    <Table responsive hover className={`mb-0 text-center ${css.table}`}>
      <thead>
        <tr>
          <th>Online</th>
          <th className="text-left">Game</th>
          <th>Port</th>
          <th className="d-none d-sm-block">Last Played</th>
        </tr>
      </thead>
      <tbody>
        { games.map(game => (
          <tr key={game.id}>
            <td>
              <i className={`fas fa-lg fa-circle ${isOnline(game) ? css.online : css.offline}`} />
            </td>
            <td className="text-left">{ game.name }</td>
            <td>{ game.port }</td>
            <td className="d-none d-sm-block">{ game.lastPlayed }</td>
          </tr>
        ))}
      </tbody>
    </Table>
  </Card>
)

export default GamesTable;
