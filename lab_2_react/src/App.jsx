import { useState } from "react";
import "./App.css";
import Nav from "./components/Nav";
import Header from "./components/Header";
import Footer from "./components/Footer";
import Education from "./components/Education";
import SoftSkills from "./components/SoftSkills";
import HardSkills from "./components/HardSkills";
import Languages from "./components/Languages";
import Projects from "./components/Projects";
import PersonalInfo from "./components/PersonalInfo";
import ProjectsPage from "./components/ProjectsPage";
import CertPage from "./components/CertPage";

function App() {
  const [currentPage, setCurrentPage] = useState("cv");

  return (
    <div className="font-[Segoe_UI,Tahoma,Geneva,Verdana,sans-serif] m-0 p-0 text-[#1f1f1f]">
      <Nav currentPage={currentPage} setPage={setCurrentPage} />

      {currentPage === "cv" && (
        <>
          <div className="ml-[150px] w-[calc(100%-150px)] box-border">
            <Header />
            <main className="block">
              <div
                className="block py-[40px] px-[20px] w-full min-h-screen box-border"
                style={{ background: "#fffbf4 url('/firework.svg') repeat", backgroundSize: "300px 300px" }}
              >
                <div className="bg-white w-full max-w-[820px] mx-auto py-[32px] px-[40px] border-none shadow-[0_10px_40px_rgba(0,0,0,0.05),0_2px_10px_rgba(242,142,43,0.05)] font-[Times_New_Roman,Times,serif] text-[#1f1f1f] leading-[1.4] box-content print:shadow-none print:max-w-none print:p-0">
                  <PersonalInfo />
                  <HardSkills />
                  <Projects />
                  <Education />
                  <Languages />
                </div>
              </div>
            </main>
            <Footer />
          </div>
        </>
      )}

      {currentPage === "projects" && <ProjectsPage />}

      {currentPage === "certs" && <CertPage />}
    </div>
  );
}

export default App;
