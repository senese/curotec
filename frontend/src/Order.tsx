import { Badge, Col, Row } from "react-bootstrap";

function Order() {
  return (
    <div className="d-flex flex-row">
      <Col className="order-index flex-shrink-1" xs="1">
        <Badge bg="secondary">1</Badge>
      </Col>
      <Col className="order-name flex-grow-1">Name</Col>
      <Col className="order-value flex-grow-1">$ {}</Col>
      <Col className="order-edit flex-shrink-1" xs="1">
        <i className="bi bi-pencil"></i>
      </Col>
      <Col className="order-remove flex-shrink-1" xs="1">
        <i className="bi bi-trash3"></i>
      </Col>
    </div>
  );
}

export default Order;
