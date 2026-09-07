import { BrowserRouter, Routes, Route } from "react-router-dom";

import Home from "./pages/Home";
import Login from "./pages/Login";
import Dashboard from "./pages/Dashboard";
import Schemes from "./pages/Schemes";
import Assistant from "./pages/Assistant";
import CivicReport from "./pages/CivicReport";
import VoiceAssistant from "./pages/VoiceAssistant";
import SchemeDetails from "./pages/SchemeDetails";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/login" element={<Login />} />
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/schemes" element={<Schemes />} />
        <Route path="/assistant" element={<Assistant />} />
        <Route path="/civic-report" element={<CivicReport />} />
        <Route path="/voice" element={<VoiceAssistant />} />
        <Route path="/scheme-details" element={<SchemeDetails />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;