import { useState } from "react";
import reactLogo from "./assets/react.svg";
import viteLogo from "/vite.svg";
import "./App.css";
import Header from "./components/Header";
import Education from "./components/Education";
import SoftSkills from "./components/SoftSkills";
import HardSkills from "./components/HardSkills";
import Languages from "./components/Languages";
import Projects from "./components/Projects";
import PersonalInfo from "./components/PersonalInfo";

function App() {
  return (
    <div>
      <Header />
      <PersonalInfo />
      <Education />
      <HardSkills />
      <SoftSkills />
      <Languages />
      <Projects />
    </div>
  );
}

export default App;
