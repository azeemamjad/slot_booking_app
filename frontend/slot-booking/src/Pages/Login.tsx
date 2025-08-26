import React, { useState } from "react";
import { useNavigate } from "react-router-dom";

const Login = () => {
  const [identifier, setIdentifier] = useState(""); // email or username
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  const navigate = useNavigate()

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    // TODO: Replace with real API call
    if (identifier && password) {
      // Simulate login
      localStorage.setItem('access-token', '300');
      if (identifier.includes("admin"))
      {
        localStorage.setItem('role', 'admin');
      }
      window.dispatchEvent(new Event("storage"));
      navigate('/');
    } else {
      setError("Please enter your email/username and password.");
    }
  };

  return (
    <div className="max-w-md mx-auto bg-white p-8 rounded shadow">
      <h2 className="text-2xl font-bold mb-4">Login</h2>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          placeholder="Email or Username"
          value={identifier}
          onChange={e => setIdentifier(e.target.value)}
          className="w-full mb-3 p-2 border rounded"
        />
        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={e => setPassword(e.target.value)}
          className="w-full mb-3 p-2 border rounded"
        />
        {error && <div className="text-red-500 mb-2">{error}</div>}
        <button type="submit" className="w-full bg-yellow-500 text-white py-2 rounded">Login</button>
      </form>
      <div className="mt-4 text-center">
        <button className="text-blue-500" onClick={() => navigate("/signup")}>Don't have an account? Sign up</button>
      </div>
    </div>
  );
};

export default Login;
