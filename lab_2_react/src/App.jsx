import { useState, useEffect } from "react";
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
import Reviews from "./components/Reviews";
import ContactForm from "./components/ContactForm";

function App() {
  const [currentPage, setCurrentPage] = useState("cv");
  const [theme, setTheme] = useState("light");

  useEffect(() => {
    const currentHour = new Date().getHours();
    if (currentHour >= 7 && currentHour < 21) {
      setTheme("light");
      document.documentElement.classList.remove('dark');
    } else {
      setTheme("dark");
      document.documentElement.classList.add('dark');
    }
  }, []);

  const toggleTheme = () => {
    const newTheme = theme === "light" ? "dark" : "light";
    setTheme(newTheme);
    if (newTheme === "dark") {
      document.documentElement.classList.add('dark');
    } else {
      document.documentElement.classList.remove('dark');
    }
  };

  return (
    <div className="font-[Segoe_UI,Tahoma,Geneva,Verdana,sans-serif] m-0 p-0 text-[#1f1f1f] dark:text-[#e0e0e0] dark:bg-[#121212] min-h-screen transition-colors duration-300">
      <Nav currentPage={currentPage} setPage={setCurrentPage} theme={theme} toggleTheme={toggleTheme} />
      <ContactForm />

      {currentPage === "cv" && (
        <>
          <div className="ml-[150px] w-[calc(100%-150px)] box-border">
            <Header />
            <main className="block">
              <div
                className={`block py-[40px] px-[20px] w-full min-h-screen box-border bg-[url('/firework.svg')] dark:bg-[url('/firework-dark.svg')] bg-[#fffbf4] dark:bg-[#121212] bg-[length:300px_300px]`}
              >
                <div className="bg-white dark:bg-white dark:text-[#1f1f1f] w-full max-w-[820px] mx-auto py-[32px] px-[40px] border-none shadow-[0_10px_40px_rgba(0,0,0,0.05),0_2px_10px_rgba(242,142,43,0.05)] dark:shadow-[0_20px_50px_rgba(0,0,0,0.8),0_0_20px_rgba(242,142,43,0.15)] dark:border-white/10 font-[Times_New_Roman,Times,serif] text-[#1f1f1f] leading-[1.4] box-content print:shadow-none print:max-w-none print:p-0 transition-colors duration-300">
                  <PersonalInfo />
                  <HardSkills />
                  <Projects />
                  <Education />
                  <Languages />
                  <Reviews />
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
