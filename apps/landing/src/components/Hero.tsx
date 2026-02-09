import React from 'react'

export const Hero = () => {
  return (
    <section className="relative pt-32 pb-20 lg:pt-48 lg:pb-32 overflow-hidden">
      {/* Background Decor */}
      <div className="absolute top-0 left-1/2 -translate-x-1/2 w-full h-full -z-10">
        <div className="absolute top-[-10%] left-[-10%] w-[40%] h-[40%] bg-brand-blue/10 rounded-full blur-[120px]" />
        <div className="absolute bottom-[10%] right-[-10%] w-[30%] h-[30%] bg-brand-cyan/10 rounded-full blur-[100px]" />
      </div>

      <div className="max-w-7xl mx-auto px-6 text-center">
        <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-brand-blue/10 border border-brand-blue/20 text-brand-blue text-sm font-bold mb-8 animate-fade-in">
          <span className="relative flex h-2 w-2">
            <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-brand-blue opacity-75"></span>
            <span className="relative inline-flex rounded-full h-2 w-2 bg-brand-blue"></span>
          </span>
          v0.4.0 Beta Now Live
        </div>

        <h1 className="text-5xl md:text-7xl font-black tracking-tight text-brand-navy dark:text-brand-light mb-6 leading-[1.1]">
          Ship bulletproof code <br />
          <span className="text-transparent bg-clip-text bg-gradient-to-r from-brand-blue to-brand-cyan">
            without the AI babysitting.
          </span>
        </h1>

        <p className="max-w-2xl mx-auto text-lg md:text-xl text-brand-slate dark:text-brand-light/70 mb-10 leading-relaxed">
          The only AI agent that self-verifies every line it writes. 
          We don't just generate code; we prove it works before you ever see a PR.
        </p>

        <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
          <a 
            href="https://github.com/Trust-WEDO" 
            className="w-full sm:w-auto px-8 py-4 bg-brand-blue text-white rounded-2xl font-bold text-lg hover:bg-brand-blue/90 hover:scale-105 transition-all shadow-lg shadow-brand-blue/25"
          >
            Get Started for Free
          </a>
          <button className="w-full sm:w-auto px-8 py-4 bg-brand-navy/5 dark:bg-brand-light/5 text-brand-navy dark:text-brand-light rounded-2xl font-bold text-lg hover:bg-brand-navy/10 dark:hover:bg-brand-light/10 transition-all border border-brand-navy/10 dark:border-brand-light/10">
            View Documentation
          </button>
        </div>

        {/* Hero Image/Mockup Placeholder */}
        <div className="mt-20 relative mx-auto max-w-5xl rounded-3xl border border-brand-navy/10 dark:border-brand-light/10 bg-white/50 dark:bg-brand-navy/50 backdrop-blur-sm p-2 shadow-2xl">
           <div className="aspect-video rounded-2xl bg-brand-navy flex items-center justify-center text-brand-light/20 font-mono text-sm overflow-hidden">
             <div className="text-left p-8 w-full h-full overflow-hidden">
                <p className="text-brand-cyan">$ trust-wedo implement auth-logic</p>
                <p className="text-brand-light/50">› Planning architecture...</p>
                <p className="text-brand-light/50">› Implementing src/auth.ts</p>
                <p className="text-brand-light/50">› Running verification tests...</p>
                <p className="text-brand-success">✅ 8/8 tests passed</p>
                <p className="text-brand-blue">› Creating PR: feat/auth-implementation</p>
                <div className="mt-4 h-full bg-brand-light/5 rounded p-4 border border-brand-light/10">
                   <div className="w-1/2 h-2 bg-brand-blue/20 rounded mb-2"></div>
                   <div className="w-3/4 h-2 bg-brand-light/10 rounded mb-2"></div>
                   <div className="w-2/3 h-2 bg-brand-light/10 rounded"></div>
                </div>
             </div>
           </div>
        </div>
      </div>
    </section>
  )
}
