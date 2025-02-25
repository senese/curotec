import { Badge, Col } from "react-bootstrap";
import IOrder from "./types/order";
import { startTransition, useState } from "react";
import { useOrders } from "./contexts/OrderProvider";
import "./styles/order.css";
import EditModal from "./components/EditModal";

interface OrderContainerProps {
  order: IOrder;
  index: number;
}

function Order({ order, index }: OrderContainerProps) {
  const [showModal, setShowModal] = useState(false);
  const { removeOrder } = useOrders();
  const handleShow = () => setShowModal(true);
  const [name, setName] = useState(order.name);
  const [value, setValue] = useState(order.value);

  function formatPrice(price: number) {
    if (typeof price === "number") {
      return price.toLocaleString("en-US", {
        style: "currency",
        currency: "USD",
        minimumFractionDigits: 2,
      });
    }
  }

  return (
    <>
      <div className="d-flex flex-row">
        <Col className="order-index flex-shrink-1" xs="1">
          <Badge bg="secondary">{index}</Badge>
        </Col>
        <Col className="order-name flex-grow-1">{name}</Col>
        <Col className="order-value flex-grow-1">{formatPrice(value)}</Col>
        <Col
          className="order-edit flex-shrink-1"
          xs="1"
          style={{ cursor: "pointer" }}
        >
          <i
            className="bi bi-pencil"
            onClick={(e) => {
              handleShow();
            }}
          ></i>
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
      <EditModal
        order={order}
        showModal={showModal}
        setShowModal={setShowModal}
      />
    </>
  );
}

export default Order;
