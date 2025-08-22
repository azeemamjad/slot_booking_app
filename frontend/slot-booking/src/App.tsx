import React from "react";
import Header from "./components/Header";
import Footer from "./components/Footer";

function App() {
  return (
    <div className="min-h-screen bg-gradient-to-b from-yellow-50 to-white flex flex-col items-center">
      <Header />

      {/* Main container */}
      <main className="flex-1 w-full max-w-5xl p-6">
        <div className="flex justify-center items-center h-64 text-gray-500 italic">
          Slot Dashboard will appear here...
        </div>
      </main>

      <Footer />
    </div>
  );
}

export default App;
