import { useEffect, useState } from "react";

function OfficeHoursAdmin() {
  const token = localStorage.getItem("token");

  const [officeHours, setOfficeHours] = useState([]);
  const [editingId, setEditingId] = useState(null);

  const [formData, setFormData] = useState({
    office_name: "",
    staff_name: "",
    day_of_week: "",
    start_time: "",
    end_time: "",
    building_id: "",
    room_id: "",
    notes: "",
  });

  useEffect(() => {
    loadOfficeHours();
  }, []);

  const loadOfficeHours = async () => {
    const response = await fetch("http://localhost:8000/admin/office-hours", {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });

    const data = await response.json();
    console.log("GET office hours:", data);

    setOfficeHours(Array.isArray(data) ? data : []);
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
      office_name: "",
      staff_name: "",
      day_of_week: "",
      start_time: "",
      end_time: "",
      building_id: "",
      room_id: "",
      notes: "",
    });
  };

  const handleAddOrUpdate = async () => {
    if (!formData.office_name || !formData.staff_name) {
      alert("Office name and staff name are required");
      return;
    }

    const payload = {
      ...formData,
      building_id: Number(formData.building_id),
      room_id: Number(formData.room_id),
    };

    console.log("Office hours payload:", payload);

    let url = "http://localhost:8000/admin/office-hours";
    let method = "POST";

    if (editingId !== null) {
      url = `http://localhost:8000/admin/office-hours/${editingId}`;
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

    const data = await response.json();
    console.log("POST/PUT office hours:", data);

    if (!response.ok) {
      alert(JSON.stringify(data));
      return;
    }

    resetForm();
    loadOfficeHours();
  };

  const handleEdit = (office) => {
    const id = office.id ?? office.office_id;

    setEditingId(id);

    setFormData({
      office_name: office.office_name ?? "",
      staff_name: office.staff_name ?? "",
      day_of_week: office.day_of_week ?? "",
      start_time: office.start_time ?? "",
      end_time: office.end_time ?? "",
      building_id: office.building_id ?? "",
      room_id: office.room_id ?? "",
      notes: office.notes ?? "",
    });
  };

  const handleDelete = async (office) => {
    const id = office.id ?? office.office_id;

    if (!window.confirm("Delete this office hour?")) return;

    await fetch(`http://localhost:8000/admin/office-hours/${id}`, {
      method: "DELETE",
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });

    loadOfficeHours();
  };

  return (
    <div style={{ marginTop: "40px" }}>
      <h2 style={{ color: "#0f172a" }}>Office Hours</h2>

      <div style={{ display: "flex", gap: "10px", flexWrap: "wrap", marginBottom: "20px" }}>
        <input
          name="office_name"
          placeholder="Office Name"
          value={formData.office_name}
          onChange={handleChange}
          style={{
            padding: "10px",
            borderRadius: "8px",
            border: "1px solid #cbd5e1",
          }}
        />
        <input
          name="staff_name"
          placeholder="Staff Name"
          value={formData.staff_name}
          onChange={handleChange}
          style={{
            padding: "10px",
            borderRadius: "8px",
            border: "1px solid #cbd5e1",
          }}
        />
        <input
          name="day_of_week"
          placeholder="Day of Week"
          value={formData.day_of_week}
          onChange={handleChange}
          style={{
            padding: "10px",
            borderRadius: "8px",
            border: "1px solid #cbd5e1",
          }}
        />
        <input
          type="time"
          name="start_time"
          value={formData.start_time}
          onChange={handleChange}
          style={{
            padding: "10px",
            borderRadius: "8px",
            border: "1px solid #cbd5e1",
          }}
        />
        <input
          type="time"
          name="end_time"
          value={formData.end_time}
          onChange={handleChange}
          style={{
            padding: "10px",
            borderRadius: "8px",
            border: "1px solid #cbd5e1",
          }}
        />
        <input
          name="building_id"
          placeholder="Building ID"
          value={formData.building_id}
          onChange={handleChange}
          style={{
            padding: "10px",
            borderRadius: "8px",
            border: "1px solid #cbd5e1",
          }}
        />
        <input
          name="room_id"
          placeholder="Room ID"
          value={formData.room_id}
          onChange={handleChange}
          style={{
            padding: "10px",
            borderRadius: "8px",
            border: "1px solid #cbd5e1",
          }}
        />
        <input
          name="notes"
          placeholder="Notes"
          value={formData.notes}
          onChange={handleChange}
          style={{
            padding: "10px",
            borderRadius: "8px",
            border: "1px solid #cbd5e1",
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
          {editingId ? "Update" : "Add"}
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
              Office
            </th>
            <th style={{ padding: "12px", border: "1px solid #94a3b8", textAlign: "left" }}>
              Staff
            </th>
            <th style={{ padding: "12px", border: "1px solid #94a3b8", textAlign: "left" }}>
              Day
            </th>
            <th style={{ padding: "12px", border: "1px solid #94a3b8", textAlign: "left" }}>
              Start
            </th>
            <th style={{ padding: "12px", border: "1px solid #94a3b8", textAlign: "left" }}>
              End
            </th>
            <th style={{ padding: "12px", border: "1px solid #94a3b8", textAlign: "left" }}>
              Building
            </th>
            <th style={{ padding: "12px", border: "1px solid #94a3b8", textAlign: "left" }}>
              Room
            </th>
            <th style={{ padding: "12px", border: "1px solid #94a3b8", textAlign: "left" }}>
              Notes
            </th>
            <th style={{ padding: "12px", border: "1px solid #94a3b8", textAlign: "left" }}>
              Actions
            </th>
          </tr>
        </thead>

        <tbody>
          {officeHours.map((office, index) => {
            const id = office.id ?? office.office_id ?? index;

            return (
              <tr key={id} style={{ background: "#f8fafc" }}>
                <td style={{ padding: "12px", border: "1px solid #cbd5e1" }}>{id}</td>
                <td style={{ padding: "12px", border: "1px solid #cbd5e1" }}>
                  {office.office_name}
                </td>
                <td style={{ padding: "12px", border: "1px solid #cbd5e1" }}>
                  {office.staff_name}
                </td>
                <td style={{ padding: "12px", border: "1px solid #cbd5e1" }}>
                  {office.day_of_week}
                </td>
                <td style={{ padding: "12px", border: "1px solid #cbd5e1" }}>
                  {office.start_time}
                </td>
                <td style={{ padding: "12px", border: "1px solid #cbd5e1" }}>
                  {office.end_time}
                </td>
                <td style={{ padding: "12px", border: "1px solid #cbd5e1" }}>
                  {office.building_id}
                </td>
                <td style={{ padding: "12px", border: "1px solid #cbd5e1" }}>
                  {office.room_id}
                </td>
                <td style={{ padding: "12px", border: "1px solid #cbd5e1" }}>
                  {office.notes}
                </td>

                <td style={{ padding: "12px", border: "1px solid #cbd5e1" }}>
                  <button
                    onClick={() => handleEdit(office)}
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
                    onClick={() => handleDelete(office)}
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

export default OfficeHoursAdmin;