import { Container, ListGroup } from "react-bootstrap";
import { useAutoAnimate } from '@formkit/auto-animate/react'
import { useEffect } from "react";
import OrderForm from "./OrderForm";
import Order from "./Order";
import { useOrders } from "./contexts/OrderProvider";

function MainPage() {
  const { orders, isLoadingOrder, getOrders } = useOrders()
  const [listGroup, enableAnimations] = useAutoAnimate()

  useEffect(() => {
    getOrders()
  }, []);

  return (
    <div>
      <Container>
        <h1>Curotec Assessment</h1>
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
