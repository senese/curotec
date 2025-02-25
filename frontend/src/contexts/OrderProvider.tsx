import React, {
  createContext,
  useState,
  ReactNode,
  useContext,
} from "react";
import IOrder from "../types/order";


interface OrdersProviderProps {
  children: ReactNode;
}

interface IOrdersContext {
  orders: IOrder[];
  isLoadingOrder: boolean;
  addOrder(name: string, value: number): void;
  getOrders(): void;
  removeOrder(order: IOrder): void;
}

const OrdersContext = createContext<IOrdersContext | undefined>(undefined);

export const OrdersProvider: React.FC<OrdersProviderProps> = ({ children }) => {
  const [isLoadingOrder, setIsLoadingOrder] = useState(false)
  const [orders, setOrders] = useState<IOrder[]>([])
  

  async function addOrder(name: string, value: number) {
    setIsLoadingOrder(true)
    fetch(process.env.REACT_APP_ORDERS_URL!, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${localStorage.getItem("access_token")}`
      },
      body: JSON.stringify({ name: name, value: value })
    })
    .then((res) => {
      if (res.ok)
        return res.json()
    })
    .then((json: unknown) => {
      
      if (!isValidOrder(json)) {
        console.error('Invalid information');
        return;
      }
      delete json.user_id
      setOrders([...orders, json])
      setIsLoadingOrder(false)
    })
    .catch(function (error) {
      console.error('Error: ' + error.message);
    });
  }

  async function removeOrder(order: IOrder) {
    fetch(`${process.env.REACT_APP_ORDERS_URL!}${order.id}`, {
      method: "DELETE",
      headers: {
        Authorization: `Bearer ${localStorage.getItem("access_token")}`
      },
    })
    .then((res) => {
      if (res.ok) {
        const filteredList = orders.filter(o => o !== order)
        setOrders(filteredList)
      }
    })
    .catch(function (error) {
      console.error('Error: ' + error.message);
    });
  }

  function isValidOrder(order: unknown): order is IOrder {
    return (
      typeof order === 'object' &&
      order !== null &&
      'id' in order &&
      'name' in order &&
      'value' in order &&
      typeof (order as IOrder).id === 'number' &&
      typeof (order as IOrder).name === 'string' &&
      typeof (order as IOrder).value === 'number'
    );
  }

  const getOrders = async () => {
    const orders = await (await fetch(`${process.env.REACT_APP_ORDERS_URL!}`, {
      headers: { Authorization: `Bearer ${localStorage.getItem("access_token")}` }
    })).json()
    console.log(orders)
    setOrders(orders)
  }

  return (
    <OrdersContext.Provider value={{ orders, isLoadingOrder, addOrder, getOrders, removeOrder }}>
      {children}
    </OrdersContext.Provider>
  );
};

export const useOrders = () => {
  const context = useContext(OrdersContext);
  if (!context) {
    throw new Error("useOrders must be used within an OrdersProvider");
  }
  return context;
};
