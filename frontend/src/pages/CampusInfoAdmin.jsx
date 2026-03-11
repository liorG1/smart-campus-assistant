import { useEffect, useState } from "react";

function CampusInfoAdmin() {
  const token = localStorage.getItem("token");

  const [items, setItems] = useState([]);
  const [editingId, setEditingId] = useState(null);

  const [formData, setFormData] = useState({
    title: "",
    category: "",
    content: "",
  });

  useEffect(() => {
    loadCampusInfo();
  }, []);

  const loadCampusInfo = async () => {
    try {
      const response = await fetch("http://localhost:8000/admin/campus-info", {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      const data = await response.json();
      console.log("GET /admin/campus-info response:", data);
      setItems(Array.isArray(data) ? data : []);
    } catch (error) {
      console.error("Error loading campus info:", error);
      alert("Failed to load campus info");
    }
  };

  const handleChange = (e) => {
    const { name, value } = e.target;

    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  const resetForm = () => {
    setEditingId(null);
    setFormData({
      title: "",
      category: "",
      content: "",
    });
  };

  const handleAddOrUpdate = async () => {
    if (!formData.title.trim() || !formData.category.trim() || !formData.content.trim()) {
      alert("Title, category and content are required");
      return;
    }

    const payload = {
      title: formData.title,
      category: formData.category,
      content: formData.content,
    };

    console.log("Campus info payload being sent:", payload);

    try {
      let url = "http://localhost:8000/admin/campus-info";
      let method = "POST";

      if (editingId !== null) {
        url = `http://localhost:8000/admin/campus-info/${editingId}`;
        method = "PUT";
      }

      const response = await fetch(url, {
        method,
        headers: {
          Authorization: `Bearer ${token}`,
          "Content-Type": "application/json",
        },
        body: JSON.stringify(payload),
      });

      const responseData = await response.json();
      console.log(
        "POST/PUT /admin/campus-info response full:",
        JSON.stringify(responseData, null, 2)
      );

      if (!response.ok) {
        alert(JSON.stringify(responseData, null, 2));
        throw new Error("Failed to save campus info");
      }

      resetForm();
      loadCampusInfo();
    } catch (error) {
      console.error("Error saving campus info:", error);
    }
  };

  const handleEdit = (item) => {
    const itemId = item.id ?? item.campus_info_id;

    setEditingId(itemId);
    setFormData({
      title: item.title ?? "",
      category: item.category ?? "",
      content: item.content ?? "",
    });
  };

  const handleDelete = async (item) => {
    const itemId = item.id ?? item.campus_info_id;

    if (!itemId) {
      console.error("Missing campus info id:", item);
      alert("Campus info ID is missing. Check console.");
      return;
    }

    const confirmDelete = window.confirm("Delete this campus info item?");
    if (!confirmDelete) return;

    try {
      const response = await fetch(
        `http://localhost:8000/admin/campus-info/${itemId}`,
        {
          method: "DELETE",
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      let responseData = null;
      try {
        responseData = await response.json();
      } catch {
        responseData = null;
      }

      console.log("DELETE /admin/campus-info response:", responseData);

      if (!response.ok) {
        alert("Delete failed");
        throw new Error("Delete failed");
      }

      loadCampusInfo();
    } catch (error) {
      console.error("Error deleting campus info:", error);
    }
  };

  return (
    <div style={{ marginTop: "40px" }}>
      <h2 style={{ color: "#0f172a" }}>Campus Info</h2>

      <div style={{ marginBottom: "20px", display: "flex", gap: "10px", flexWrap: "wrap" }}>
        <input
          type="text"
          name="title"
          placeholder="Title"
          value={formData.title}
          onChange={handleChange}
          style={{
            padding: "10px",
            borderRadius: "8px",
            border: "1px solid #cbd5e1",
          }}
        />

        <input
          type="text"
          name="category"
          placeholder="Category"
          value={formData.category}
          onChange={handleChange}
          style={{
            padding: "10px",
            borderRadius: "8px",
            border: "1px solid #cbd5e1",
          }}
        />

        <input
          type="text"
          name="content"
          placeholder="Content"
          value={formData.content}
          onChange={handleChange}
          style={{
            padding: "10px",
            borderRadius: "8px",
            border: "1px solid #cbd5e1",
            minWidth: "260px",
          }}
        />

        <button
          onClick={handleAddOrUpdate}
          style={{
            padding: "10px 16px",
            borderRadius: "8px",
            border: "none",
            background: "#16a34a",
            color: "white",
            cursor: "pointer",
          }}
        >
          {editingId ? "Update Info" : "Add Info"}
        </button>

        {editingId && (
          <button
            onClick={resetForm}
            style={{
              padding: "10px 16px",
              borderRadius: "8px",
              border: "none",
              background: "#64748b",
              color: "white",
              cursor: "pointer",
            }}
          >
            Cancel
          </button>
        )}
      </div>

      <table
        style={{
          width: "100%",
          borderCollapse: "collapse",
          marginTop: "12px",
          background: "white",
          color: "#0f172a",
        }}
      >
        <thead>
          <tr style={{ background: "#cbd5e1" }}>
            <th style={{ padding: "12px", border: "1px solid #94a3b8", textAlign: "left" }}>
              ID
            </th>
            <th style={{ padding: "12px", border: "1px solid #94a3b8", textAlign: "left" }}>
              Title
            </th>
            <th style={{ padding: "12px", border: "1px solid #94a3b8", textAlign: "left" }}>
              Category
            </th>
            <th style={{ padding: "12px", border: "1px solid #94a3b8", textAlign: "left" }}>
              Content
            </th>
            <th style={{ padding: "12px", border: "1px solid #94a3b8", textAlign: "left" }}>
              Actions
            </th>
          </tr>
        </thead>

        <tbody>
          {items.map((item, index) => {
            const itemId = item.id ?? item.campus_info_id ?? `row-${index}`;

            return (
              <tr key={itemId} style={{ background: "#f8fafc" }}>
                <td style={{ padding: "12px", border: "1px solid #cbd5e1" }}>
                  {item.id ?? item.campus_info_id ?? "-"}
                </td>

                <td style={{ padding: "12px", border: "1px solid #cbd5e1" }}>
                  {item.title ?? "-"}
                </td>

                <td style={{ padding: "12px", border: "1px solid #cbd5e1" }}>
                  {item.category ?? "-"}
                </td>

                <td style={{ padding: "12px", border: "1px solid #cbd5e1" }}>
                  {item.content ?? "-"}
                </td>

                <td style={{ padding: "12px", border: "1px solid #cbd5e1" }}>
                  <button
                    onClick={() => handleEdit(item)}
                    style={{
                      marginRight: "8px",
                      padding: "8px 12px",
                      borderRadius: "8px",
                      border: "none",
                      background: "#2563eb",
                      color: "white",
                      cursor: "pointer",
                    }}
                  >
                    Edit
                  </button>

                  <button
                    onClick={() => handleDelete(item)}
                    style={{
                      padding: "8px 12px",
                      borderRadius: "8px",
                      border: "none",
                      background: "#dc2626",
                      color: "white",
                      cursor: "pointer",
                    }}
                  >
                    Delete
                  </button>
                </td>
              </tr>
            );
          })}
        </tbody>
      </table>
    </div>
  );
}

export default CampusInfoAdmin;