import React from 'react';
import { useRouter } from 'next/router';
import { Container,
         Card,
         CardBody,
         Form,
         FormGroup,
         FormFeedback,
         Label,
         Input,
         Col,
         Row } from 'reactstrap';
import Layout from '../components/Layout';
import useForm from 'react-hook-form';
import ThemeButton from '../components/ThemeButton';
import Link from 'next/link';
import api from '../api';


const Login = props => {
  const router = useRouter();
  const { register, handleSubmit, errors } = useForm();

  const onSubmit = async data => {
    await api.user.register(data);
    router.push('/login')
  }

  const usernameCheck = async value => {
    try {
      await api.user.getUser(value);
      return false;
    } catch (e) {
      return e.status === 404
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
                <h3 className="mb-4">Register</h3>
                <Form onSubmit={handleSubmit(onSubmit)}>
                  <FormGroup>
                    <Label for="username">Username</Label>
                    <Input type="text" 
                           id="username"
                           name="username"
                           placeholder="username"
                           invalid={Boolean(errors.username)}
                           innerRef={register({ 
                             required: 'username is required',
                             minLength: {
                               value: 5,
                               message: 'username must be at least 5 characters'
                             },
                             maxLength: {
                               value: 20,
                               message: 'username can be at most 20 characters'
                             },
                             pattern: {
                                value: /^[a-zA-Z0-9]+$/,
                                message: 'only letters and numbers allowed'
                             },
                             validate: {
                               usernameTaken: usernameCheck
                             }
                           })} />
                    { errors.username &&
                      <FormFeedback>
                        { errors.username.type == 'usernameTaken' ?
                            "username taken" :
                            errors.username.message
                        }</FormFeedback>
                    }
                  </FormGroup>
                  <FormGroup>
                    <Label for="password">Password</Label>
                    <Input type="password"
                           id="password"
                           name="password"
                           placeholder="password"
                           invalid={Boolean(errors.password)}
                           innerRef={register({ 
                             required: 'password is required',
                             minLength: {
                               value: 5,
                               message: 'password must be at least 5 characters'
                             }
                           })} />
                    { errors.password &&
                      <FormFeedback>{ errors.password.message }</FormFeedback>
                    }
                  </FormGroup>
                  <div className="mt-4">
                    <ThemeButton outline type="submit">Register</ThemeButton>
                    <Link href="/login">
                      <a>
                        <ThemeButton color="link">Login</ThemeButton>
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
