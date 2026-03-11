import ChatBox from "../components/ChatBox";
import PageContainer from "../components/PageContainer";
function Home() {
  return (
    <PageContainer>
    <div style={{ padding: "40px 20px" }}>
      <div style={{ 'maxWidth': "900px", margin: "0 auto", textAlign: "center" }}>
        <h1 style={{ marginBottom: "10px", color: "#0f172a" }}>
          Student Assistant Chat
        </h1>

        <p style={{ color: "#334155", marginBottom: "30px" }}>
          Ask about exams, rooms, office hours, and campus information
        </p>

        <ChatBox />
      </div>
    </div>
    </PageContainer>
  );
}

export default Home;