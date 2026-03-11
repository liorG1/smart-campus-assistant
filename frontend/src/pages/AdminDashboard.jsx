import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import ExamsAdmin from "./ExamsAdmin";
import CoursesAdmin from "./CoursesAdmin";
import OfficeHoursAdmin from "./OfficeHoursAdmin";
import CampusInfoAdmin from "./CampusInfoAdmin";
import PageContainer from "../components/PageContainer";
function AdminDashboard() {
  const navigate = useNavigate();
  const [token, setToken] = useState(localStorage.getItem("token"));
  const [isCheckingAuth, setIsCheckingAuth] = useState(true);

  useEffect(() => {
    const savedToken = localStorage.getItem("token");

    if (!savedToken) {
      navigate("/admin-login");
      return;
    }

    setToken(savedToken);
    setIsCheckingAuth(false);
  }, [navigate]);

  const handleLogout = () => {
    localStorage.removeItem("token");
    setToken(null);
    navigate("/admin-login");
  };

  if (isCheckingAuth) {
    return (
      <div
        style={{
          padding: "40px 20px",
          background: "#f5f7fb",
          minHeight: "100vh",
          color: "#0f172a",
        }}
      >
        Checking authentication...
      </div>
    );
  }

  if (!token) {
    return null;
  }

  return (
    <PageContainer>
    <div style={{ padding: "40px 20px", background: "#f5f7fb", minHeight: "100vh" }}>
      <div
        style={{
          maxWidth: "1100px",
          margin: "0 auto",
          background: "white",
          padding: "30px",
          borderRadius: "16px",
          boxShadow: "0 8px 30px rgba(0,0,0,0.08)",
        }}
      >
        <div
          style={{
            display: "flex",
            justifyContent: "space-between",
            alignItems: "center",
            marginBottom: "20px",
            flexWrap: "wrap",
            gap: "12px",
          }}
        >
          <div>
            <h1 style={{ margin: 0, color: "#0f172a" }}>Admin Dashboard</h1>
            <p style={{ marginTop: "8px", color: "#334155" }}>
              Manage campus information from here
            </p>
          </div>

          <button
            onClick={handleLogout}
            style={{
              padding: "10px 16px",
              borderRadius: "10px",
              border: "none",
              background: "#0f172a",
              color: "white",
              cursor: "pointer",
              fontWeight: "600",
            }}
          >
            Logout
          </button>
        </div>

        <div
          style={{
            marginTop: "20px",
            padding: "16px",
            borderRadius: "12px",
            background: "#f8fafc",
            border: "1px solid #cbd5e1",
            color: "#0f172a",
          }}
        >
          <strong>Token status:</strong>{" "}
          <span style={{ color: "#166534", fontWeight: "600" }}>
            Admin authenticated
          </span>
        </div>

        <ExamsAdmin />
        <CoursesAdmin />
        <OfficeHoursAdmin />
        <CampusInfoAdmin />
      </div>
    </div>
    </PageContainer>
  );
}

export default AdminDashboard;