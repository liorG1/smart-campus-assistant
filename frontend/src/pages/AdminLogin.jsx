import { useState } from "react";
import PageContainer from "../components/PageContainer";
function AdminLogin() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");

  const handleLogin = async () => {
    try {
      const formData = new URLSearchParams();
      formData.append("username", username);
      formData.append("password", password);

      const response = await fetch("http://localhost:8000/admin/login", {
        method: "POST",
        headers: {
          "Content-Type": "application/x-www-form-urlencoded",
        },
        body: formData,
      });

      const data = await response.json();
      console.log("Login response:", data);

      if (response.ok && data.access_token) {
        localStorage.setItem("token", data.access_token);
        alert("Login successful");
        window.location.href = "/admin";
      } else {
        alert(data.detail || "Login failed");
      }
    } catch (error) {
      console.error("Login error:", error);
      alert("Server error during login");
    }
  };

  return (
     <PageContainer>
    <div style={{ padding: "40px 20px" }}>
      <div
        style={{
          maxWidth: "420px",
          margin: "40px auto",
          background: "white",
          padding: "30px",
          borderRadius: "16px",
          boxShadow: "0 8px 30px rgba(0,0,0,0.08)",
        }}
      >
        <h2 style={{ textAlign: "center", marginBottom: "24px" }}>Admin Login</h2>

        <input
          type="text"
          placeholder="Username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          style={{
            width: "100%",
            padding: "12px",
            marginBottom: "14px",
            borderRadius: "10px",
            border: "1px solid #cbd5e1",
            boxSizing: "border-box",
          }}
        />

        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          style={{
            width: "100%",
            padding: "12px",
            marginBottom: "18px",
            borderRadius: "10px",
            border: "1px solid #cbd5e1",
            boxSizing: "border-box",
          }}
        />

        <button
          onClick={handleLogin}
          style={{
            width: "100%",
            padding: "12px",
            borderRadius: "10px",
            border: "none",
            background: "#0f172a",
            color: "white",
            fontWeight: "bold",
            cursor: "pointer",
          }}
        >
          Login
        </button>
      </div>
    </div>
    </PageContainer>
  );
}

export default AdminLogin;