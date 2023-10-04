import './App.css';
import {BrowserRouter, Routes, Route} from "react-router-dom";
import RecordMUI from './pages/RecordMUI';

// to add a differnt path, such as home, add a route and set component in element.
function App() {
  return (
    <div className='App'>
      <BrowserRouter>
        <Routes>
          <Route path ="/" element={<RecordMUI />}/>
          {/* <Route path ="/audio_recorder" element={<AudioRecorder />}/> */}
        </Routes>
      </BrowserRouter>

    </div>
  );
}

export default App;
