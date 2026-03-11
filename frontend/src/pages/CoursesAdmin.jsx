import { useEffect, useState } from "react";

function CoursesAdmin() {
  const token = localStorage.getItem("token");

  const [courses, setCourses] = useState([]);
  const [editingId, setEditingId] = useState(null);

  const [formData, setFormData] = useState({
    course_name: "",
    course_code: "",
  });

  useEffect(() => {
    loadCourses();
  }, []);

  const loadCourses = async () => {
    try {
      const response = await fetch("http://localhost:8000/admin/courses", {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      const data = await response.json();
      console.log("GET /admin/courses response:", data);
      setCourses(Array.isArray(data) ? data : []);
    } catch (error) {
      console.error("Error loading courses:", error);
      alert("Failed to load courses");
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
      course_name: "",
      course_code: "",
    });
  };

  const handleAddOrUpdate = async () => {
    if (!formData.course_name.trim() || !formData.course_code.trim()) {
      alert("Course name and course code are required");
      return;
    }

    const payload = {
      course_name: formData.course_name,
      course_code: formData.course_code,
    };

    console.log("Course payload being sent:", payload);

    try {
      let url = "http://localhost:8000/admin/courses";
      let method = "POST";

      if (editingId !== null) {
        url = `http://localhost:8000/admin/courses/${editingId}`;
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
        "POST/PUT /admin/courses response full:",
        JSON.stringify(responseData, null, 2)
      );

      if (!response.ok) {
        alert(JSON.stringify(responseData, null, 2));
        throw new Error("Failed to save course");
      }

      resetForm();
      loadCourses();
    } catch (error) {
      console.error("Error saving course:", error);
    }
  };

  const handleEdit = (course) => {
    const courseId = course.course_id ?? course.id;

    setEditingId(courseId);
    setFormData({
      course_name: course.course_name ?? "",
      course_code: course.course_code ?? "",
    });
  };

  const handleDelete = async (course) => {
    const courseId = course.course_id ?? course.id;

    if (!courseId) {
      console.error("Missing course id:", course);
      alert("Course ID is missing. Check console.");
      return;
    }

    const confirmDelete = window.confirm("Delete this course?");
    if (!confirmDelete) return;

    try {
      const response = await fetch(
        `http://localhost:8000/admin/courses/${courseId}`,
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

      console.log("DELETE /admin/courses response:", responseData);

      if (!response.ok) {
        alert("Delete failed");
        throw new Error("Delete failed");
      }

      loadCourses();
    } catch (error) {
      console.error("Error deleting course:", error);
    }
  };

  return (
    <div style={{ marginTop: "40px" }}>
      <h2 style={{ color: "#0f172a" }}>Courses</h2>

      <div style={{ marginBottom: "20px", display: "flex", gap: "10px", flexWrap: "wrap" }}>
        <input
          type="text"
          name="course_name"
          placeholder="Course name"
          value={formData.course_name}
          onChange={handleChange}
          style={{
            padding: "10px",
            borderRadius: "8px",
            border: "1px solid #cbd5e1",
          }}
        />

        <input
          type="text"
          name="course_code"
          placeholder="Course code"
          value={formData.course_code}
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
          {editingId ? "Update Course" : "Add Course"}
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
              Course
            </th>
            <th style={{ padding: "12px", border: "1px solid #94a3b8", textAlign: "left" }}>
              Code
            </th>
            <th style={{ padding: "12px", border: "1px solid #94a3b8", textAlign: "left" }}>
              Actions
            </th>
          </tr>
        </thead>

        <tbody>
          {courses.map((course, index) => {
            const courseId = course.course_id ?? course.id ?? `row-${index}`;

            return (
              <tr key={courseId} style={{ background: "#f8fafc" }}>
                <td style={{ padding: "12px", border: "1px solid #cbd5e1" }}>
                  {course.course_id ?? course.id ?? "-"}
                </td>

                <td style={{ padding: "12px", border: "1px solid #cbd5e1" }}>
                  {course.course_name ?? "-"}
                </td>

                <td style={{ padding: "12px", border: "1px solid #cbd5e1" }}>
                  {course.course_code ?? "-"}
                </td>

                <td style={{ padding: "12px", border: "1px solid #cbd5e1" }}>
                  <button
                    onClick={() => handleEdit(course)}
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
                    onClick={() => handleDelete(course)}
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

export default CoursesAdmin;