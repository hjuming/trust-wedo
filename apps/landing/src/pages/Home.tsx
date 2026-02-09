import React from 'react'
import { Navigation } from '../components/Navigation'
import { Hero } from '../components/Hero'
import { Footer } from '../components/Footer'

const Features = () => {
  const features = [
    {
      title: 'Self-Verification Loop',
      desc: 'Automated testing and verification built into every task. If it fails, we fix it.',
      icon: '🔄',
    },
    {
      title: 'Deep Context Awareness',
      desc: 'We index your entire repository to understand your project structure and standards.',
      icon: '🧠',
    },
    {
      title: 'Multi-Step Autonomy',
      desc: 'From planning to PR, handle complex workflows without constant supervision.',
      icon: '🚀',
    },
  ]

  return (
    <section className="py-24 bg-white dark:bg-brand-navy/30">
      <div className="max-w-7xl mx-auto px-6">
        <div className="grid md:grid-cols-3 gap-12">
          {features.map((f) => (
            <div key={f.title} className="p-8 rounded-3xl border border-brand-navy/5 dark:border-brand-light/5 hover:border-brand-blue/20 transition-all group">
              <div className="text-4xl mb-6 group-hover:scale-110 transition-transform inline-block">
                {f.icon}
              </div>
              <h3 className="text-xl font-bold text-brand-navy dark:text-brand-light mb-4">
                {f.title}
              </h3>
              <p className="text-brand-slate dark:text-brand-light/60 leading-relaxed">
                {f.desc}
              </p>
            </div>
          ))}
        </div>
      </div>
    </section>
  )
}

export default function Home() {
  return (
    <div className="min-h-screen bg-brand-light dark:bg-brand-navy transition-colors duration-300">
      <Navigation />
      <main>
        <Hero />
        <Features />
        {/* Other sections would go here */}
      </main>
      <Footer />
    </div>
  )
}
