function PageContainer({ children }) {
  return (
    <div
      style={{
        width: "100%",
        padding: "40px",
        background: "#f5f7fb",
        minHeight: "100vh",
      }}
    >
      <div
        style={{
          width: "100%",
          background: "white",
          padding: "30px",
          borderRadius: "16px",
          boxShadow: "0 8px 30px rgba(0,0,0,0.08)",
        }}
      >
        {children}
      </div>
    </div>
  );
}

export default PageContainer;