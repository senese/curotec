import { Container, ListGroup } from "react-bootstrap";
import { useEffect } from "react";
import OrderForm from "./OrderForm";
import Order from "./Order";

function MainPage() {
  useEffect(() => {}, []);

  return (
    <div>
      <Container>
        <h1>Curotec Assessment</h1>
        <OrderForm />
        <div className="border rounded-3 p-3">
          <h4>Your orders</h4>
          <ListGroup>
            <ListGroup.Item>
              <Order/>
            </ListGroup.Item>
          </ListGroup>
        </div>
      </Container>
    </div>
  );
}

export default MainPage;
