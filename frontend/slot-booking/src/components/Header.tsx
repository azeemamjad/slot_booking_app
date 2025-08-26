import { useNavigate } from "react-router-dom";

const navItems = [{"name": "Dashboard", "url": "/"}, {"name": "Bookings", "url": "/bookings"}, {"name":"Profile", "url": "/profile"}];
const authItems = [{"name": "Login", "url": "/login"}, {"name": "Signup", "url": "/signup"}];

// Some nice random star colors

function Header() {

  const navigate = useNavigate()

  return (
    <header className="relative w-full bg-yellow-400 shadow-md p-4 text-center overflow-hidden">
      <div className="flex justify-center items-center">
        <div>
          <h1 className="text-3xl font-bold text-white">🎮 Daily Slot Booking</h1>
          <p className="text-sm text-yellow-100">Book your daily slot — fair and fun!</p>

          {/* Navigation */}
          { localStorage.getItem("access-token")?
           (<>
           <nav className="mt-3 flex justify-center gap-6 text-white font-medium">
            {navItems.map((item, idx) => (
              <button key={idx} className="cursor-pointer hover:underline" onClick={() => navigate(item.url)}>
                {item.name}
              </button>
            ))}
          </nav>
          </>):
          (<>
          <nav className="mt-3 flex justify-center gap-6 text-white font-medium">
            {authItems.map((item, idx) => (
              <button key={idx} className="cursor-pointer hover:underline" onClick={() => navigate(item.url)}>
                {item.name}
              </button>
            ))}
          </nav>
          </>)}
          
      </div>
      {localStorage.getItem('access-token') && 
      (<div className="ml-28 text-amber-100 h-12 w-25 flex justify-center items-center">
        <button onClick={
          () => {
            localStorage.removeItem('access-token');
            navigate("/login");
          }
        } className="h-10 w-20 bg-red-500 flex items-center justify-center hover:h-12 hover:w-25 transition-all cursor-pointer">Logout</button>
      </div>)
      }
    </div>
    </header>
  );
}

export default Header;



