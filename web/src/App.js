import './App.css';
import Home from './pages/Home';
import Record from './pages/Record';
import {BrowserRouter, Routes, Route} from "react-router-dom";


function App() {
  return (
    <div className='App'>
      <BrowserRouter>
        <Routes>
          <Route path ="/" element={<Home />}/>
          <Route path ="/record" element={<Record />}/>
        </Routes>
      </BrowserRouter>

    </div>
  );
}

export default App;
