import { Button, Col, Form, Row, Spinner } from "react-bootstrap";
import { useEffect, useState } from "react";

const OrderForm = () => {
  const [name, setName] = useState("");
  const [value, setValue] = useState("");
  const [loading, setLoading] = useState(false);

  const handleNameChange = (e) => setName(e.target.value);
  const handleValueChange = (e) => setValue(e.target.value);

  const handleSubmission = async (e) => {
    e.preventDefault();
    setLoading(true);
  };

  useEffect(() => {}, []);

  return (
    <>
      <Form onSubmit={handleSubmission} className="mb-4">
        <Row>
          <Col>
            <Form.Group controlId="formName" className="mb-3">
              <Form.Label>Name</Form.Label>
              <Form.Control
                type="text"
                placeholder="Order name"
                value={name}
                onChange={handleNameChange}
                required
              />
            </Form.Group>
          </Col>

          <Col>
            <Form.Group controlId="formValue" className="mb-3">
              <Form.Label>Value</Form.Label>
              <Form.Control
                type="number"
                placeholder="Order value"
                value={value}
                onChange={handleValueChange}
                required
              />
            </Form.Group>
          </Col>

          <Row>
            <Col xs="auto">
              <Button
                variant="primary"
                type="submit"
                disabled={loading}
                >
                {loading ? (
                  "Submitting..."
                ) : (
                  "Submit"
                )}
              </Button>
              </Col>
          </Row>
        </Row>
      </Form>
    </>
  );
};

export default OrderForm;
