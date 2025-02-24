import { BrowserRouter, Routes, Route } from "react-router";
import { OrdersProvider } from "./contexts/OrderProvider";
import { PrivateRoute } from "./PrivateRoute";
import { AuthProvider } from "./contexts/AuthProvider";
import MainPage from "./MainPage";
import LoginPage from "./LoginPage";

function App() {
  return (
    <>
      <AuthProvider>
        <OrdersProvider>
          <BrowserRouter>
            <Routes>
              <Route path="/" element={<PrivateRoute><MainPage /></PrivateRoute>}/>
              <Route path="/auth" element={<LoginPage/>}/>
            </Routes>
          </BrowserRouter>
        </OrdersProvider>
      </AuthProvider>
    </>
  );
}

export default App;
