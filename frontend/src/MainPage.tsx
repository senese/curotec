import { Button, Container, Form, ListGroup, ListGroupItem, Modal, Row } from "react-bootstrap";
import { useAutoAnimate } from '@formkit/auto-animate/react'
import { useEffect, useState } from "react";
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
              <ListGroupItem key={order.id}>
                <Order
                  order={order}
                  index={index+1}
                />
              </ListGroupItem>
            )
          }
          </ListGroup>
        </div>
      </Container>
    </div>
  );
}

export default MainPage;
