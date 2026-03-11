import { BrowserRouter, Routes, Route, Link } from "react-router-dom";
import Home from "./pages/Home";
import AdminLogin from "./pages/AdminLogin";
import AdminDashboard from "./pages/AdminDashboard";

function App() {
  return (
    <BrowserRouter>
      <div style={{ minHeight: "100vh", background: "#f5f7fb" }}>
        <nav
          style={{
            display: "flex",
            justifyContent: "space-between",
            alignItems: "center",
            padding: "16px 24px",
            background: "#0f172a",
            color: "white",
          }}
        >
          <h2 style={{ margin: 0 }}>Smart Campus Assistant</h2>

          <div style={{ display: "flex", gap: "12px" }}>
            <Link
              to="/"
              style={{ color: "white", textDecoration: "none", fontWeight: "bold" }}
            >
              Student Chat
            </Link>

            <Link
              to="/admin-login"
              style={{ color: "white", textDecoration: "none", fontWeight: "bold" }}
            >
              Admin Login
            </Link>

            <Link
              to="/admin"
              style={{ color: "white", textDecoration: "none", fontWeight: "bold" }}
            >
              Admin Dashboard
            </Link>
          </div>
        </nav>

        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/admin-login" element={<AdminLogin />} />
          <Route path="/admin" element={<AdminDashboard />} />
        </Routes>
      </div>
    </BrowserRouter>
  );
}

export default App;