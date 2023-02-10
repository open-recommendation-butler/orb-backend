import { BrowserRouter, Routes, Route } from "react-router-dom";
import Navbar from './components/navbar';
import Footer from './components/footer';
import LandingPage from './pages/landingPage';
import SearchPage from './pages/searchPage';

function App() {
  return (
    <BrowserRouter>
      <Navbar />
      <Routes>
        <Route index path="/" element={<LandingPage />} />
        <Route path="/search" element={<SearchPage />} />
      </Routes>
      <Footer />
    </BrowserRouter>
  );
}

export default App;
