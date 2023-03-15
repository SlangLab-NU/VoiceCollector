
import './App.css';
import Home from './components/Home';
import AboutUs from './components/AboutUs';
import NavBar from './components/NavBar';
import Footer from './components/Footer';
import ContactUs from './components/ContactUs';
import { Animator, ScrollContainer, ScrollPage, batch, Fade, FadeIn, FadeOut, Move, MoveIn, MoveOut, Sticky, StickyIn, StickyOut, Zoom, ZoomIn, ZoomOut } from "react-scroll-motion";


function App() {
  return (
    <div className="App">
      <NavBar />
      <ScrollContainer>
        <ScrollPage>
          <Animator animation={batch(MoveIn(0,200), MoveOut())}>
              <Home />
          </Animator>
        </ScrollPage>

        <ScrollPage>
          <Animator animation={batch(Fade(), Sticky(), MoveOut(0, -200))}>
              <AboutUs />
          </Animator>
        </ScrollPage>

        <ScrollPage>
          <Animator animation={batch( FadeIn())}>
              <ContactUs />
          </Animator>
        </ScrollPage>
      </ScrollContainer>
    <Footer/>

    </div>
  );
}

export default App;
