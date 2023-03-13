import './App.css';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import RecordPage from './components/RecordPage';
import HomePage from './components/HomePage';

function App() {
  return (
    <BrowserRouter>
      <div className='App'>
        <main>
          <Routes>
            <Route path='/record' element={<RecordPage />} />
            <Route path='/' element={<HomePage />} />
          </Routes>
        </main>
      </div>
    </BrowserRouter>
  );
}

export default App;
