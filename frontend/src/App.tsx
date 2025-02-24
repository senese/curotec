import { BrowserRouter, Routes, Route } from "react-router";
import MainPage from "./MainPage";

function App() {
  return (
    <>
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<MainPage />}></Route>
        </Routes>
      </BrowserRouter>
    </>
  );
};

export default App;
