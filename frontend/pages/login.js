import React, { useState, useContext } from 'react';
import nookies from 'nookies';
import { useRouter } from 'next/router';
import { Container,
         Card,
         CardBody,
         Form,
         FormGroup,
         Label,
         Input,
         Col,
         Row } from 'reactstrap';
import Layout from '../components/Layout';
import ThemeButton from '../components/ThemeButton';
import useForm from '../hooks/useForm';
import api from '../api';
import UserContext from '../ctx/UserContext';


const Login = props => {
  const router = useRouter();
  const { loginUser } = useContext(UserContext);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null)
  const { values, onChange } = useForm({
    username: '',
    password: ''
  })
  const { username, password } = values;


  const onSubmit = async e => {
    if (e) e.preventDefault();
    setLoading(true);
    setError(null)

    try {
      await loginUser(username, password);
      setLoading(false);
      router.push('/')
    }
    catch (e) {
      setError(e.toString())
      setLoading(false)
    }
  }

  return (
    <Layout>
      <Container>
        <Row>
          <Col xs="12" sm={{size: 10, offset: 1}}
                       md={{size: 8, offset: 2}}
                       lg={{size: 6, offset: 3}}>
            <Card className="p-4 mt-5">
              <CardBody>
                <Form onSubmit={onSubmit}>
                  <FormGroup>
                    <Label for="username">Username</Label>
                    <Input type="text" 
                           id="username"
                           name="username"
                           placeholder="Username"
                           value={username}
                           onChange={onChange} />
                  </FormGroup>
                  <FormGroup>
                    <Label for="password">Password</Label>
                    <Input type="password" 
                           id="password"
                           name="password"
                           placeholder="Password"
                           value={password}
                           onChange={onChange} />
                  </FormGroup>
                  <div className="mt-4">
                    { error &&
                      <div className="text-error">{ error }</div>
                    }
                    <ThemeButton type="submit" outline disabled={loading}>Login</ThemeButton>
                    <ThemeButton color="link">Register</ThemeButton>
                  </div>
                </Form>
              </CardBody>
            </Card>
          </Col>
        </Row>
      </Container>
    </Layout>
  )
}

export default Login;
