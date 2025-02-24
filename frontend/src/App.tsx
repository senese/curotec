import { BrowserRouter, Routes, Route } from "react-router";
import { OrdersProvider } from "./contexts/OrderProvider";
import MainPage from "./MainPage";

function App() {
  return (
    <>
      <BrowserRouter>
        <OrdersProvider>
          <Routes>
            <Route path="/" element={<MainPage />}></Route>
          </Routes>
        </OrdersProvider>
      </BrowserRouter>
    </>
  );
}

export default App;
