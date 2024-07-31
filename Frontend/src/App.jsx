import React from 'react';
import {BrowserRouter as Router, Routes, Route} from 'react-router-dom';
import Navbar from "../src/components/Navbar";
import Login from "../src/components/Login";
import Signup from "../src/components/Signup";
import Admin from "../src/components/Admin";
import "tailwindcss/tailwind.css";


function App() {
  return (
    <Router>
      <Navbar/>
      <Routes>

      {/* <Route path="/" element={<Home />} /> */}
            {/* <Route path="/spaces" element={<Spaces />} /> */}
            {/* <Route path="/researches" element={<Researches />} />
            <Route path="/about" element={<About />} />
            <Route path="/contact" element={<Contact />} /> */}
            <Route path="/signup" element={<Signup />} />
            <Route path="/login" element={<Login />} />
            <Route path="/Admin" element={<Admin />} />
     </Routes>
    </Router>
  )
};
export default App
