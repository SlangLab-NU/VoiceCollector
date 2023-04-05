import './App.css';
import Home from './pages/Home';
import Record from './pages/Record';
import AudioRecorder from './components/AudioRecorder';
import {BrowserRouter, Routes, Route} from "react-router-dom";


function App() {
  return (
    <div className='App'>
      <BrowserRouter>
        <Routes>
          <Route path ="/" element={<Home />}/>
          <Route path ="/record" element={<Record />}/>
          <Route path ="/audio_recorder" element={<AudioRecorder />}/>
        </Routes>
      </BrowserRouter>

    </div>
  );
}

export default App;
