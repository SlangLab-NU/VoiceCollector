import './App.css';
import Home from './pages/Home';
import RecordMUI from './pages/RecordMUI';
import {BrowserRouter, Routes, Route} from "react-router-dom";


function App() {
  return (
    <div className='App'>
      <BrowserRouter>
        <Routes>
          <Route path ="/" element={<Home />}/>
          <Route path ="/record" element={<RecordMUI />}/>

        </Routes>
      </BrowserRouter>

    </div>
  );
}

export default App;
