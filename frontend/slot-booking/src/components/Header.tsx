import React, { useState, useEffect } from "react";
import { motion } from "framer-motion";

const navItems = ["Dashboard", "Bookings", "Admin", "Profile"];

// Some nice random star colors
const starColors = ["#FFD700", "#FF69B4", "#7FFFD4", "#FF4500", "#87CEFA"];

function Header() {
  const [mousePos, setMousePos] = useState({ x: 0, y: 0 });

  // Track mouse movement globally
  useEffect(() => {
    const handleMouseMove = (e: MouseEvent) => {
      setMousePos({ x: e.clientX, y: e.clientY });
    };
    window.addEventListener("mousemove", handleMouseMove);
    return () => window.removeEventListener("mousemove", handleMouseMove);
  }, []);

  return (
    <header className="relative w-full bg-yellow-400 shadow-md p-4 text-center overflow-hidden">
      <h1 className="text-3xl font-bold text-white">🎮 Tekken 8 Slot Booking</h1>
      <p className="text-sm text-yellow-100">Book your daily slot — fair and fun!</p>

      {/* Navigation */}
      <nav className="mt-3 flex justify-center gap-6 text-white font-medium">
        {navItems.map((item, idx) => (
          <div key={idx} className="cursor-pointer hover:underline">
            {item}
          </div>
        ))}
      </nav>

      {/* Floating stars following mouse */}
      {[...Array(5)].map((_, starIdx) => (
        <motion.span
          key={starIdx}
          className="absolute pointer-events-none text-xl"
          style={{ color: starColors[starIdx % starColors.length] }}
          initial={{ opacity: 0 }}
          animate={{
            x: mousePos.x + Math.random() * 40 - 20, // small random offset
            y: mousePos.y + Math.random() * 40 - 20,
            opacity: [0, 1, 0],
          }}
          transition={{
            duration: 1.2,
            delay: starIdx * 0.1,
            repeat: Infinity,
          }}
        >
          ⭐
        </motion.span>
      ))}
    </header>
  );
}

export default Header;
