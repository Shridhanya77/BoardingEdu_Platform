import Navbar from '../components/Navbar'
import Footer from '../components/Footer'
import useMouseSpotlight from '../hooks/useMouseSpotlight'
import useClickRipple from '../hooks/useClickRipple'
import useStaggeredReveal from '../hooks/useStaggeredReveal'

export default function MainLayout({ children }) {
  useMouseSpotlight()
  useClickRipple()
  useStaggeredReveal()

  return (
    <div className="d-flex flex-column min-vh-100">
      <Navbar />
      <main className="flex-grow-1">{children}</main>
      <Footer />
    </div>
  )
}
