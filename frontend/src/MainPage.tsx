import { Button, Container, ListGroup, Row } from "react-bootstrap";
import { useAutoAnimate } from '@formkit/auto-animate/react'
import { useEffect } from "react";
import OrderForm from "./OrderForm";
import Order from "./Order";
import { useOrders } from "./contexts/OrderProvider";
import { useAuth } from "./contexts/AuthProvider";

function MainPage() {
  const { orders, isLoadingOrder, getOrders } = useOrders()
  const [listGroup, enableAnimations] = useAutoAnimate()
  const { logout } = useAuth()

  useEffect(() => {
    getOrders()
  }, []);

  return (
    <div>
      <Container>
        <div className="d-flex">
          <div className="justify-self-start flex-grow-1">
            <h1>Curotec Assessment</h1>
          </div>
          <div className="justify-self-end align-self-center">
            <Button className="col"
              variant="outline-primary"
              onClick={() => {logout()}}
              >
              Logout
            </Button>
          </div>
        </div>
        <OrderForm />
        <div className="border rounded-3 p-3">
          <h4>Your orders</h4>
          <ListGroup ref={listGroup} className="list-group-flush">
          { (orders) && 
            orders?.map((order, index) =>
              <Order
                key={order.id}
                order={order}
                index={index+1}
              />
            )
          }
          </ListGroup>
        </div>
      </Container>
    </div>
  );
}

export default MainPage;
