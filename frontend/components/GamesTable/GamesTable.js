import React from 'react';
import Link from 'next/link';
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
        </tr>
      </thead>
      <tbody>
        { games.map(game => (
          <Link key={game.id} href={`/game/${game.slug}`}>
            <tr>
              <td>
                <i className={`fas fa-lg fa-circle ${isOnline(game) ? css.online : css.offline}`} />
              </td>
              <td className="text-left">{ game.server_name }</td>
              <td>{ game.port }</td>
            </tr>
          </Link>
        ))}
      </tbody>
    </Table>
  </Card>
)

export default GamesTable;
