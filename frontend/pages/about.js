import React from 'react';
import { Container, Col } from 'reactstrap';
import { IndexJumbo } from '../components/Jumbo';
import Layout from '../components/Layout';


const About = props => {

  return (
    <Layout>
      <IndexJumbo />

      <Container>
        <Col xs={12} sm={{size: 10, offset: 1}} lg={{size: 8, offset: 2}} style={{lineHeight: 2.5}}>
          <h2>What is this thing?</h2>
          <p>Termninja is a set of games that are played via a termnial. Players connect using something like netcat and all of the logic, rendering and input handling is done by the server.</p>

          <h2>Ways to Play</h2>
          <p>The recommended way to play termninja games is using the provided client script.</p>

          <h5>Installation</h5>
          <ul>
            <li><code>sudo curl -X GET https://www.term.ninja/client -o /usr/local/bin/termninja</code></li>
            <li><code>sudo chmod +x /usr/local/bin/termninja</code></li>
            <li>Note: if you aren't comfortable using sudo to install globally, change -o to a path you have write permission to and run it from there.</li>
          </ul>
          <h5>Usage</h5>          
          <p className="ml-3">
            <code>termninja --help</code>
            <p>show available options</p>

            <code>termninja</code>
            <p>connect and play - choose a game when prompted</p>

            <code>termninja -l</code>
            <p>login to track scores and compete for the leaderboard</p>

            <code>termninja -g 1 -i</code>
            <p>play snake. some real-time games require -i so input will be sent immediately. -g specifies index of a game to autostart.</p>

            <code>termninja -g 2 -a</code>
            <p>play tic-tac-toe anonymously. even if logged in, -a will play anonymously.</p>
          </p>

          <h5>Other ways to play</h5>
          <p className="ml-3">
            <p>These commands are what the client script build for you. You can be a true ninja and run them manually.</p>
            <p>
              <div>basic</div>
              <code>openssl s_client -async -quiet -connect play.term.ninja:3333 2>/dev/null</code>
            </p>

            <p>
              <div>real-time (e.g. snake)</div>
              <code>stty -icanon && openssl s_client -async -quiet -connect play.term.ninja:3333 2>/dev/null</code>
            </p>

            <p>
              <div>login</div>
              <code>curl -X POST -d username=username&password=password https://play.term.ninja/auth/obtain_play_token</code>
            </p>
          </p>
        </Col>
      </Container>
    </Layout>
  )
}

export default About;