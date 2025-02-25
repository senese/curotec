import { Badge, Col } from "react-bootstrap";
import IOrder from "./types/order";
import { startTransition } from "react";
import { useOrders } from "./contexts/OrderProvider";
import "./styles/order.css"

interface OrderContainerProps {
  order: IOrder;
  index: number;
}

function Order({ order, index }: OrderContainerProps) {
  const { removeOrder } = useOrders();
  const handleShow = () => setShowModal(true);

  function formatPrice(price: number) {
    if (typeof price === "number") {
      return price.toLocaleString("pt-BR", {
        style: "currency",
        currency: "USD",
        minimumFractionDigits: 2,
      });
    }
  }

  return (
    <div className="d-flex flex-row">
      <Col className="order-index flex-shrink-1" xs="1">
        <Badge bg="secondary">{index}</Badge>
      </Col>
      <Col className="order-name flex-grow-1">{order.name}</Col>
        <Col className="order-value flex-grow-1">{formatPrice(order.value)}</Col>
      <Col
        className="order-edit flex-shrink-1"
        xs="1"
        style={{ cursor: "pointer" }}
      >
        <i className="bi bi-pencil"></i>
      </Col>
      <Col
        className="order-remove flex-shrink-1"
        xs="1"
        style={{ cursor: "pointer" }}
      >
        <i
          className="bi bi-trash3"
          onClick={(e) => {
            startTransition(() => {
              removeOrder(order);
            });
          }}
        ></i>
      </Col>
    </div>
  );
}

export default Order;
