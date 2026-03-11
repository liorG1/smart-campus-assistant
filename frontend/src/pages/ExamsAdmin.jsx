import { useEffect, useState } from "react";

function ExamsAdmin() {
  const token = localStorage.getItem("token");

  const [exams, setExams] = useState([]);
  const [loading, setLoading] = useState(true);
  const [courses, setCourses] = useState([]);
  const [rooms, setRooms] = useState([]);
  const [editingExamId, setEditingExamId] = useState(null);

  const [formData, setFormData] = useState({
    course_id: "",
    exam_date: "",
    exam_time: "",
    room_id: "",
    notes: "",
  });

  useEffect(() => {
    loadExams();
    loadCourses();
    loadRooms();
  }, []);

  const loadExams = async () => {
    try {
      setLoading(true);

      const response = await fetch("http://localhost:8000/admin/exams", {
        method: "GET",
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      if (!response.ok) {
        throw new Error("Failed to load exams");
      }

      const data = await response.json();
      console.log("GET /admin/exams response:", data);
      setExams(Array.isArray(data) ? data : []);
    } catch (error) {
      console.error("Error loading exams:", error);
      alert("Failed to load exams");
    } finally {
      setLoading(false);
    }
  };

  const loadCourses = async () => {
    try {
      const response = await fetch("http://localhost:8000/admin/courses", {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      const data = await response.json();
      setCourses(Array.isArray(data) ? data : []);
    } catch (error) {
      console.error("Error loading courses:", error);
    }
  };

  const loadRooms = async () => {
    try {
      const response = await fetch("http://localhost:8000/admin/rooms", {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      const data = await response.json();
      setRooms(Array.isArray(data) ? data : []);
    } catch (error) {
      console.error("Error loading rooms:", error);
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
    setFormData({
      course_id: "",
      exam_date: "",
      exam_time: "",
      room_id: "",
      notes: "",
    });
    setEditingExamId(null);
  };

  const handleAddOrUpdate = async () => {
    if (
      !formData.course_id ||
      !formData.exam_date ||
      !formData.exam_time ||
      !formData.room_id
    ) {
      alert("Please fill course, exam date, exam time and room");
      return;
    }

    const payload = {
      course_id: Number(formData.course_id),
      exam_date: formData.exam_date,
      exam_time: formData.exam_time,
      room_id: Number(formData.room_id),
      notes: formData.notes || "",
    };

    console.log("Payload being sent:", payload);

    try {
      let response;

      if (editingExamId !== null) {
        response = await fetch(
          `http://localhost:8000/admin/exams/${editingExamId}`,
          {
            method: "PUT",
            headers: {
              Authorization: `Bearer ${token}`,
              "Content-Type": "application/json",
            },
            body: JSON.stringify(payload),
          }
        );
      } else {
        response = await fetch("http://localhost:8000/admin/exams", {
          method: "POST",
          headers: {
            Authorization: `Bearer ${token}`,
            "Content-Type": "application/json",
          },
          body: JSON.stringify(payload),
        });
      }

      const responseData = await response.json();
      console.log("POST/PUT response full:", JSON.stringify(responseData, null, 2));

      if (!response.ok) {
        alert(JSON.stringify(responseData, null, 2));
        throw new Error("Request failed");
      }

      resetForm();
      loadExams();
    } catch (error) {
      console.error("Error saving exam:", error);
      alert("Failed to save exam");
    }
  };

  const handleEdit = (exam) => {
    const examId = exam.exam_id ?? exam.id;

    setEditingExamId(examId);
    setFormData({
      course_id: exam.course_id ?? "",
      exam_date: exam.exam_date ?? "",
      exam_time: exam.exam_time ?? "",
      room_id: exam.room_id ?? "",
      notes: exam.notes ?? "",
    });
  };

  const handleDelete = async (exam) => {
    const examId = exam.exam_id ?? exam.id;

    if (!examId) {
      console.error("Delete failed: exam id is missing", exam);
      alert("Exam ID is missing. Check console.");
      return;
    }

    const confirmDelete = window.confirm("Are you sure you want to delete this exam?");
    if (!confirmDelete) return;

    try {
      const response = await fetch(
        `http://localhost:8000/admin/exams/${examId}`,
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

      console.log("DELETE response:", responseData);

      if (!response.ok) {
        alert("Delete failed");
        throw new Error("Delete failed");
      }

      loadExams();
    } catch (error) {
      console.error("Error deleting exam:", error);
      alert("Failed to delete exam");
    }
  };

  return (
    <div style={{ marginTop: "30px" }}>
      <h2 style={{ color: "#0f172a" }}>Exam Schedules</h2>

      <div
        style={{
          marginTop: "20px",
          padding: "20px",
          borderRadius: "14px",
          background: "#f8fafc",
          border: "1px solid #e2e8f0",
        }}
      >
        <h3 style={{ marginTop: 0, color: "#0f172a" }}>
          {editingExamId ? "Edit Exam" : "Add Exam"}
        </h3>

        <div
          style={{
            display: "grid",
            gridTemplateColumns: "repeat(auto-fit, minmax(220px, 1fr))",
            gap: "14px",
          }}
        >
          <div>
            <label style={{ display: "block", marginBottom: "6px", color: "#334155" }}>
              Course
            </label>
            <select
              name="course_id"
              value={formData.course_id}
              onChange={handleChange}
              style={{
                width: "100%",
                padding: "10px",
                borderRadius: "8px",
                border: "1px solid #cbd5e1",
              }}
            >
              <option value="">Select course</option>
              {courses.map((course) => (
                <option
                  key={course.course_id ?? course.id}
                  value={course.course_id ?? course.id}
                >
                  {course.course_name}
                </option>
              ))}
            </select>
          </div>

          <div>
            <label style={{ display: "block", marginBottom: "6px", color: "#334155" }}>
              Exam Date
            </label>
            <input
              type="date"
              name="exam_date"
              value={formData.exam_date}
              onChange={handleChange}
              style={{
                width: "100%",
                padding: "10px",
                borderRadius: "8px",
                border: "1px solid #cbd5e1",
              }}
            />
          </div>

          <div>
            <label style={{ display: "block", marginBottom: "6px", color: "#334155" }}>
              Exam Time
            </label>
            <input
              type="time"
              name="exam_time"
              value={formData.exam_time}
              onChange={handleChange}
              style={{
                width: "100%",
                padding: "10px",
                borderRadius: "8px",
                border: "1px solid #cbd5e1",
              }}
            />
          </div>

          <div>
            <label style={{ display: "block", marginBottom: "6px", color: "#334155" }}>
              Room
            </label>
            <select
              name="room_id"
              value={formData.room_id}
              onChange={handleChange}
              style={{
                width: "100%",
                padding: "10px",
                borderRadius: "8px",
                border: "1px solid #cbd5e1",
              }}
            >
              <option value="">Select room</option>
              {rooms.map((room) => (
                <option
                  key={room.room_id ?? room.id}
                  value={room.room_id ?? room.id}
                >
                  {room.room_name ?? room.name ?? `Room ${room.room_id ?? room.id}`}
                </option>
              ))}
            </select>
          </div>

          <div>
            <label style={{ display: "block", marginBottom: "6px", color: "#334155" }}>
              Notes
            </label>
            <input
              type="text"
              name="notes"
              value={formData.notes}
              onChange={handleChange}
              placeholder="Optional notes"
              style={{
                width: "100%",
                padding: "10px",
                borderRadius: "8px",
                border: "1px solid #cbd5e1",
              }}
            />
          </div>
        </div>

        <div style={{ marginTop: "18px", display: "flex", gap: "10px", flexWrap: "wrap" }}>
          <button
            onClick={handleAddOrUpdate}
            style={{
              padding: "12px 18px",
              borderRadius: "10px",
              border: "none",
              background: editingExamId ? "#f59e0b" : "#16a34a",
              color: "white",
              cursor: "pointer",
              fontWeight: "600",
            }}
          >
            {editingExamId ? "Update Exam" : "Add Exam"}
          </button>

          {editingExamId && (
            <button
              onClick={resetForm}
              style={{
                padding: "12px 18px",
                borderRadius: "10px",
                border: "none",
                background: "#64748b",
                color: "white",
                cursor: "pointer",
                fontWeight: "600",
              }}
            >
              Cancel Edit
            </button>
          )}
        </div>
      </div>

      <div style={{ marginTop: "30px" }}>
        <h3 style={{ color: "#0f172a" }}>All Exam Schedules</h3>

        {loading ? (
          <p style={{ color: "#475569" }}>Loading exams...</p>
        ) : exams.length === 0 ? (
          <p style={{ color: "#475569" }}>No exams found.</p>
        ) : (
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
                  Exam ID
                </th>
                <th style={{ padding: "12px", border: "1px solid #94a3b8", textAlign: "left" }}>
                  Course
                </th>
                <th style={{ padding: "12px", border: "1px solid #94a3b8", textAlign: "left" }}>
                  Room
                </th>
                <th style={{ padding: "12px", border: "1px solid #94a3b8", textAlign: "left" }}>
                  Exam Date
                </th>
                <th style={{ padding: "12px", border: "1px solid #94a3b8", textAlign: "left" }}>
                  Exam Time
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
              {exams.map((exam, index) => {
                const examId = exam.exam_id ?? exam.id ?? `row-${index}`;

                const courseName =
                  courses.find(
                    (course) => (course.course_id ?? course.id) === exam.course_id
                  )?.course_name || exam.course_id;

                const roomName =
                  rooms.find((room) => (room.room_id ?? room.id) === exam.room_id)
                    ?.room_name ||
                  rooms.find((room) => (room.room_id ?? room.id) === exam.room_id)?.name ||
                  exam.room_id;

                return (
                  <tr key={examId} style={{ background: "#f8fafc" }}>
                    <td style={{ padding: "12px", border: "1px solid #cbd5e1" }}>
                      {exam.exam_id ?? exam.id ?? "-"}
                    </td>
                    <td style={{ padding: "12px", border: "1px solid #cbd5e1" }}>
                      {courseName}
                    </td>
                    <td style={{ padding: "12px", border: "1px solid #cbd5e1" }}>
                      {roomName}
                    </td>
                    <td style={{ padding: "12px", border: "1px solid #cbd5e1" }}>
                      {exam.exam_date}
                    </td>
                    <td style={{ padding: "12px", border: "1px solid #cbd5e1" }}>
                      {exam.exam_time || "-"}
                    </td>
                    <td style={{ padding: "12px", border: "1px solid #cbd5e1" }}>
                      {exam.notes || "-"}
                    </td>
                    <td style={{ padding: "12px", border: "1px solid #cbd5e1" }}>
                      <button
                        onClick={() => handleEdit(exam)}
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
                        onClick={() => handleDelete(exam)}
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
        )}
      </div>
    </div>
  );
}

export default ExamsAdmin;