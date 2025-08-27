import { Routes, Route } from "react-router-dom";

import Header from "./components/Header";
import Footer from "./components/Footer";

import ProtectedRoute from "./ProtectedRoute";
import AuthRoute from "./AuthRoutes";

import Dashboard from "./Pages/Dashboard";
import BookingPage from "./Pages/Bookings";

import Login from "./Pages/Login";
import Signup from "./Pages/Signup";
import ProfilePage from "./Pages/Profile";

function App() {
  return (
    <div className="min-h-screen bg-gradient-to-b from-yellow-50 to-white flex flex-col items-center">
        <Header />
        <div className="flex-grow">
          <Routes>
            {/* Authentication Routes  */}
            <Route path="/login" element={<AuthRoute children={<Login />} />} ></Route>
            <Route path="/signup" element={<AuthRoute children={<Signup />} />} ></Route>

            {/* Application Routes */}
            <Route path="/" element={<ProtectedRoute children={<Dashboard />} />} ></Route>
            <Route path="/bookings" element={<ProtectedRoute children={<BookingPage />} />} ></Route>
            <Route path="/profile" element={<ProtectedRoute children={<ProfilePage />} />} ></Route>
          </Routes>
        </div>
      <Footer />
    </div>
  );
}

export default App;


