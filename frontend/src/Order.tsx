import { Badge, Col } from "react-bootstrap";
import IOrder from "./types/order";

interface OrderContainerProps {
  order: IOrder;
  index: number;
}

function Order({ order, index }: OrderContainerProps) {
  return (
    <div className="d-flex flex-row">
      <Col className="order-index flex-shrink-1" xs="1">
        <Badge bg="secondary">{index}</Badge>
      </Col>
      <Col className="order-name flex-grow-1">{order.name}</Col>
      <Col className="order-value flex-grow-1">$ {order.value}</Col>
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
