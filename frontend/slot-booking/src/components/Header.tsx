import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

interface NavItem {
  name: string;
  url: string;
}

function Header() {
  const navigate = useNavigate();

  const defaultNavItems: NavItem[] = [
    { name: "Dashboard", url: "/" },
    { name: "Bookings", url: "/bookings" },
    { name: "Profile", url: "/profile" },
  ];

  const authItems: NavItem[] = [
    { name: "Login", url: "/login" },
    { name: "Signup", url: "/signup" },
  ];

  const [role, setRole] = useState<string>(
    localStorage.getItem("role") ?? "normal"
  );
  const [isLoggedIn, setIsLoggedIn] = useState<boolean>(
    !!localStorage.getItem("access-token")
  );

  const navItems: NavItem[] = [
    ...defaultNavItems,
    ...(role === "admin" ? [{ name: "Admin", url: "/admin" }] : []),
  ];

  // keep role + login in sync with localStorage
  useEffect(() => {
    const handleStorageChange = () => {
      setRole(localStorage.getItem("role") ?? "normal");
      setIsLoggedIn(!!localStorage.getItem("access-token"));
    };

    window.addEventListener("storage", handleStorageChange);
    return () => window.removeEventListener("storage", handleStorageChange);
  }, []);

  const handleLogout = () => {
    localStorage.removeItem("access-token");
    localStorage.removeItem("role");
    setRole("normal");
    setIsLoggedIn(false);
    navigate("/login");
  };

  return (
    <header className="relative w-full bg-yellow-400 shadow-md p-4 text-center overflow-hidden">
      <div className="flex justify-center items-center">
        <div>
          <h1 className="text-3xl font-bold text-white">
            🎮 Daily Slot Booking
          </h1>
          <p className="text-sm text-yellow-100">
            Book your daily slot — fair and fun!
          </p>

          {/* Navigation */}
          <nav className="mt-3 flex justify-center gap-6 text-white font-medium">
            {isLoggedIn
              ? navItems.map((item, idx) => (
                  <button
                    key={idx}
                    className="cursor-pointer hover:underline"
                    onClick={() => navigate(item.url)}
                  >
                    {item.name}
                  </button>
                ))
              : authItems.map((item, idx) => (
                  <button
                    key={idx}
                    className="cursor-pointer hover:underline"
                    onClick={() => navigate(item.url)}
                  >
                    {item.name}
                  </button>
                ))}
          </nav>
        </div>

        {/* Logout button */}
        {isLoggedIn && (
          <div className="ml-28 text-amber-100 h-12 w-25 flex justify-center items-center">
            <button
              onClick={handleLogout}
              className="h-10 w-20 bg-red-500 flex items-center justify-center hover:h-12 hover:w-25 transition-all cursor-pointer"
            >
              Logout
            </button>
          </div>
        )}
      </div>
    </header>
  );
}

export default Header;
