import Nav from '@/components/Nav'
import Hero from '@/components/Hero'
import Benefits from '@/components/Benefits'
import HowItWorks from '@/components/HowItWorks'
import Quoter from '@/components/Quoter'
import Footer from '@/components/Footer'

export default function Home() {
  return (
    <main className="min-h-screen bg-nomi-bg">
      <Nav />
      <Hero />
      <Benefits />
      <HowItWorks />
      <Quoter />
      <Footer />
    </main>
  )
}
