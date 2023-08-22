import { BrowserRouter, Route, Routes } from "react-router-dom";
import Home from "./pages/Home";
import Authenticte from "./pages/Authenticate";
import Navbar from "./components/Navbar";
import Register from "./pages/Register";
import { Notifications } from '@mantine/notifications';
import Dashboard from "./pages/Dashboard";

function App() {
  return (
    <>
      <BrowserRouter>
      <Notifications position='bottom-center' />
        <Navbar/>
        <Routes>
          <Route path="/" element={<Home/>} />
          <Route path="/login" element={<Authenticte/>} />
          <Route path="/register" element={<Register/>} />
          <Route path="/dashboard" element={<Dashboard/>}/>
        </Routes>
      </BrowserRouter>
    </>
  )
}

export default App
