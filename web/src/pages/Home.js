import Hero from '../components/Hero';
import AboutUs from '../components/AboutUs';
import NavBar from '../components/NavBar';
import Footer from '../components/Footer';
import ContactUs from '../components/ContactUs';
import {
  Animator,
  ScrollContainer,
  ScrollPage,
  batch,
  Fade,
  FadeIn,
  FadeOut,
  Move,
  MoveIn,
  MoveOut,
  Sticky,
  StickyIn,
  StickyOut,
  Zoom,
  ZoomIn,
  ZoomOut,
} from 'react-scroll-motion';

export default function Home() {
  return (
    <>
      <NavBar />
      <Hero/>
      <AboutUs/>
      <ContactUs/>
      {/* <ScrollContainer>
        <ScrollPage>
          <Animator animation={batch(MoveIn(0, 200), MoveOut())}>
            <Hero />
          </Animator>
        </ScrollPage>

        <ScrollPage>
          <Animator animation={batch(Fade(), Sticky(), MoveOut(0, -200))}>
            <AboutUs />
          </Animator>
        </ScrollPage>

        <ScrollPage>
          <Animator animation={batch(FadeIn())}>
            <ContactUs />
          </Animator>
        </ScrollPage>
      </ScrollContainer> */}
      <Footer />
    </>
  )
}
