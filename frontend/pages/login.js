import React, { useContext } from 'react';
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
import useForm from 'react-hook-form';
import UserContext from '../ctx/UserContext';
import Link from 'next/link';


const Login = props => {
  const router = useRouter();
  const { user, login } = useContext(UserContext)
  const { register, handleSubmit, errors } = useForm();  

  const onSubmit = async ({ username, password }) => {
    try {
      await login(username, password);
      router.push('/')
    } catch (e) {
      console.log(e)
      setError(e.toString())
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
              <h3 className="mb-4">Login</h3>
                <Form onSubmit={handleSubmit(onSubmit)}>
                  <FormGroup>
                    <Label for="username">Username</Label>
                    <Input type="text" 
                           id="username"
                           name="username"
                           placeholder="Username"
                           invalid={Boolean(errors.username)}
                           innerRef={register({ required: true })} />
                  </FormGroup>
                  <FormGroup>
                    <Label for="password">Password</Label>
                    <Input type="password" 
                           id="password"
                           name="password"
                           placeholder="Password"
                           invalid={Boolean(errors.password)}
                           innerRef={register({ required: true })} />
                  </FormGroup>
                  <div className="mt-4">
                    <ThemeButton outline>Login</ThemeButton>
                    <Link href="/register">
                      <a>
                        <ThemeButton color="link">Register</ThemeButton>
                      </a>
                    </Link>
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
