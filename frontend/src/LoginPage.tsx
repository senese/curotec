import { useState } from "react";
import { Button, Form, Container, Row, Col, Spinner } from "react-bootstrap";
import { useNavigate } from 'react-router';
import { useAuth } from "./contexts/AuthProvider";
import toast, { Toaster } from 'react-hot-toast';

function LoginPage() {
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [showForm, setShowForm] = useState(false);
  const [isCreating, setIsCreating] = useState(false);
  const [loading, setLoading] = useState(false);
  const { login, createUser } = useAuth();
  const navigate = useNavigate();

  const handleNameChange = (e) => setName(e.target.value);
  const handleEmailChange = (e) => setEmail(e.target.value);
  const handlePasswordChange = (e) => setPassword(e.target.value);

  const handleLogin = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      await login(email, password);
      navigate("/");
    } catch (error) {
      console.log(error);
    } finally {
      setLoading(false);
    }
  };

  const handleCreateAccount = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      await createUser(name, email, password)
      toast.success("User successfully registered!")
    } catch (error) {
      console.log(error)
      toast.error("Something went wrong")
    } finally {
      setLoading(false);
      setIsCreating(false)
    }
  };

  const handleShowForm = (creating = false) => {
    setIsCreating(creating);
    setShowForm(true);
  };

  const welcomeMessage = "Login or Sign in";

  return (
    <div className="login-wrapper">
      <div><Toaster/></div>
      <Container className="d-flex flex-column justify-content-center align-items-center h-100">
      <Row className="w-100">
        <h2 id="title" className="title text-center pt-2">{ welcomeMessage }</h2>
      </Row>
      <Row className="w-100 flex-grow-1 align-items-center">
          <Col>
            <div className={`form-container ${showForm ? 'visible' : 'hidden'}`}>
              <Form onSubmit={isCreating ? handleCreateAccount : handleLogin}>

                <Form.Group controlId="formName" className="mb-3" hidden={!isCreating}>
                  <Form.Label>Name</Form.Label>
                  <Form.Control
                    type="text"
                    placeholder="Your name"
                    value={name}
                    onChange={handleNameChange}
                    required={isCreating}
                  />
                </Form.Group>

                <Form.Group controlId="formEmail" className="mb-3">
                  <Form.Label>Email</Form.Label>
                  <Form.Control
                    type="email"
                    placeholder="example@email.com"
                    value={email}
                    onChange={handleEmailChange}
                    required
                  />
                </Form.Group>

                <Form.Group controlId="formPassword" className="mb-4">
                  <Form.Label>Password</Form.Label>
                  <Form.Control
                    type="password"
                    placeholder="********"
                    value={password}
                    onChange={handlePasswordChange}
                    required
                  />
                </Form.Group>

                <Button
                  variant="primary"
                  type="submit"
                  className="w-100 mb-3"
                  disabled={loading}
                >
                  {loading ? 
                  (
                    <Spinner animation="border" size="sm" />
                  ) : 
                  (
                    isCreating ? "Create account" : "Sign in"
                  )}
                </Button>

                <Button
                  variant="link"
                  className="w-100"
                  onClick={() => {
                    isCreating? handleShowForm(false) : handleShowForm(true)}
                  }
                >
                  {isCreating? "Log in" : "Register"}
                </Button>
              </Form>
            </div>
          </Col>
        </Row>
      </Container>
    </div>
  );
}

export default LoginPage;
