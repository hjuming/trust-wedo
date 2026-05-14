import { Footer } from '../components/Footer'
import { Navigation } from '../components/Navigation'
import { PricingSection } from '../components/PricingSection'

export default function Pricing() {
  return (
    <div className="min-h-screen bg-brand-navy">
      <Navigation />
      <main className="pt-20">
        <PricingSection />
      </main>
      <Footer />
    </div>
  )
}
