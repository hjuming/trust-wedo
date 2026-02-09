import React from 'react'

const footerLinks = [
  {
    title: 'Product',
    links: [
      { name: 'Features', href: '#' },
      { name: 'Pricing', href: '#' },
      { name: 'Documentation', href: '#' },
      { name: 'Changelog', href: '#' },
    ],
  },
  {
    title: 'Company',
    links: [
      { name: 'About', href: '#' },
      { name: 'Blog', href: '#' },
      { name: 'Privacy', href: '#' },
      { name: 'Terms', href: '#' },
    ],
  },
  {
    title: 'Community',
    links: [
      { name: 'GitHub', href: '#' },
      { name: 'Discord', href: '#' },
      { name: 'Twitter', href: '#' },
    ],
  },
]

export const Footer = () => {
  return (
    <footer className="bg-brand-light dark:bg-brand-navy pt-20 pb-10 border-t border-brand-navy/5 dark:border-brand-light/5">
      <div className="max-w-7xl mx-auto px-6">
        <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-5 gap-12 mb-16">
          <div className="col-span-2 lg:col-span-2">
            <div className="flex items-center gap-2 mb-6">
              <img src="/logo-icon.svg" alt="Logo" className="w-8 h-8" />
              <span className="text-xl font-black tracking-tighter text-brand-navy dark:text-brand-light">
                Trust <span className="text-brand-blue">WEDO</span>
              </span>
            </div>
            <p className="text-brand-slate dark:text-brand-light/60 max-w-sm mb-8">
              The trustworthy agentic coding partner that takes ownership of your codebase and self-verifies every change.
            </p>
            <div className="flex gap-4">
               {/* Social Icons Placeholder */}
               <div className="w-10 h-10 rounded-full bg-brand-navy/5 dark:bg-brand-light/5 flex items-center justify-center hover:bg-brand-blue/10 transition-colors cursor-pointer">
                  <span className="text-xs">𝕏</span>
               </div>
               <div className="w-10 h-10 rounded-full bg-brand-navy/5 dark:bg-brand-light/5 flex items-center justify-center hover:bg-brand-blue/10 transition-colors cursor-pointer">
                  <span className="text-xs">GH</span>
               </div>
            </div>
          </div>
          
          {footerLinks.map((group) => (
            <div key={group.title}>
              <h3 className="font-bold text-brand-navy dark:text-brand-light mb-6">
                {group.title}
              </h3>
              <ul className="space-y-4">
                {group.links.map((link) => (
                  <li key={link.name}>
                    <a 
                      href={link.href} 
                      className="text-brand-slate dark:text-brand-light/60 hover:text-brand-blue dark:hover:text-brand-cyan transition-colors"
                    >
                      {link.name}
                    </a>
                  </li>
                ))}
              </ul>
            </div>
          ))}
        </div>
        
        <div className="pt-10 border-t border-brand-navy/5 dark:border-brand-light/5 flex flex-col md:flex-row justify-between items-center gap-4">
          <p className="text-sm text-brand-slate dark:text-brand-light/40">
            © 2024 Trust WEDO. All rights reserved.
          </p>
          <div className="text-sm text-brand-slate dark:text-brand-light/40">
            Version: Landing v1.0 (Beta)
          </div>
        </div>
      </div>
    </footer>
  )
}
