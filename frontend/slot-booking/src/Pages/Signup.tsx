import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";


const Signup = () => {
  const [email, setEmail] = useState("");
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [department, setDepartment] = useState("");
  const [departments, setDepartments] = useState<string[]>([]);
  const [error, setError] = useState("");

  const navigate = useNavigate();

  useEffect(() => {
    // TODO: Replace with real API call
    setDepartments(["CSE", "ECE", "ME", "CE"]); // Example departments
  }, []);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (email && username && password && department) {
      // Simulate signup
      console.log("To Be Implemented")
    } else {
      setError("Please fill all fields.");
    }
  };

  return (
    <div className="max-w-md mx-auto bg-white p-8 rounded shadow">
      <h2 className="text-2xl font-bold mb-4">Sign Up</h2>
      <form onSubmit={handleSubmit}>
        <input
          type="email"
          placeholder="Email"
          value={email}
          onChange={e => setEmail(e.target.value)}
          className="w-full mb-3 p-2 border rounded"
        />
        <input
          type="text"
          placeholder="Username"
          value={username}
          onChange={e => setUsername(e.target.value)}
          className="w-full mb-3 p-2 border rounded"
        />
        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={e => setPassword(e.target.value)}
          className="w-full mb-3 p-2 border rounded"
        />
        <select
          value={department}
          onChange={e => setDepartment(e.target.value)}
          className="w-full mb-3 p-2 border rounded"
        >
          <option value="">Select Department</option>
          {departments.map(dep => (
            <option key={dep} value={dep}>{dep}</option>
          ))}
        </select>
        {error && <div className="text-red-500 mb-2">{error}</div>}
        <button type="submit" className="w-full bg-yellow-500 text-white py-2 rounded">Sign Up</button>
      </form>
      <div className="mt-4 text-center">
        <button className="text-blue-500" onClick={() => navigate("/login")}>Already have an account? Login</button>
      </div>
    </div>
  );
};

export default Signup;
