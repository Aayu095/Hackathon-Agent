'use client'

import { motion } from 'framer-motion'
import { useRouter } from 'next/navigation'
import { Zap, ArrowLeft, Play } from 'lucide-react'

export default function DemoPage() {
  const router = useRouter()

  return (
    <div className="min-h-screen bg-black text-white overflow-hidden">
      {/* Animated background */}
      <div className="fixed inset-0 animated-gradient opacity-50" />
      
      {/* Grid overlay */}
      <div className="fixed inset-0 bg-[linear-gradient(rgba(255,255,255,.03)_1px,transparent_1px),linear-gradient(90deg,rgba(255,255,255,.03)_1px,transparent_1px)] bg-[size:100px_100px]" />

      {/* Content */}
      <div className="relative z-10">
        {/* Navigation */}
        <motion.nav
          initial={{ y: -100 }}
          animate={{ y: 0 }}
          transition={{ duration: 0.6 }}
          className="container mx-auto px-6 py-6 flex items-center justify-between"
        >
          <div className="flex items-center space-x-2">
            <Zap className="w-8 h-8 text-white" />
            <span className="text-2xl font-bold shimmer">Hackathon Agent</span>
          </div>
          <button
            onClick={() => router.push('/landing')}
            className="flex items-center space-x-2 px-6 py-2 text-white/80 hover:text-white transition-colors"
          >
            <ArrowLeft className="w-4 h-4" />
            <span>Back</span>
          </button>
        </motion.nav>

        {/* Demo Section */}
        <section className="container mx-auto px-6 py-20">
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
            className="max-w-5xl mx-auto text-center mb-12"
          >
            <h1 className="text-5xl md:text-7xl font-bold mb-6">
              See It In <span className="shimmer">Action</span>
            </h1>
            <p className="text-xl text-white/60 max-w-2xl mx-auto">
              Watch how Hackathon Agent transforms the way teams approach and win hackathons
            </p>
          </motion.div>

          {/* Video Player */}
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8, delay: 0.2 }}
            className="max-w-5xl mx-auto"
          >
            <div className="relative aspect-video bg-white/5 border border-white/10 rounded-2xl glass overflow-hidden group">
              {/* Placeholder for video */}
              <div className="absolute inset-0 flex items-center justify-center">
                <div className="text-center">
                  <div className="w-24 h-24 bg-white/10 rounded-full flex items-center justify-center mx-auto mb-4 group-hover:bg-white/20 transition-all cursor-pointer">
                    <Play className="w-12 h-12 text-white" />
                  </div>
                  <p className="text-white/60">Demo video coming soon</p>
                  <p className="text-sm text-white/40 mt-2">3 minutes • Full walkthrough</p>
                </div>
              </div>
            </div>
          </motion.div>

          {/* Features Highlight */}
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8, delay: 0.4 }}
            className="max-w-4xl mx-auto mt-20 grid md:grid-cols-3 gap-8"
          >
            {[
              { title: 'Idea Validation', description: 'Search 10,000+ past projects' },
              { title: 'Real-time Tracking', description: 'Monitor GitHub commits live' },
              { title: 'Auto Presentations', description: 'Generate pitch decks instantly' }
            ].map((feature, index) => (
              <div
                key={index}
                className="p-6 bg-white/5 border border-white/10 rounded-xl glass text-center"
              >
                <h3 className="text-xl font-bold mb-2">{feature.title}</h3>
                <p className="text-white/60">{feature.description}</p>
              </div>
            ))}
          </motion.div>

          {/* CTA */}
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8, delay: 0.6 }}
            className="text-center mt-16"
          >
            <button
              onClick={() => router.push('/signup')}
              className="px-10 py-5 bg-white text-black rounded-lg hover:bg-white/90 transition-all glow-white font-bold text-xl"
            >
              Start Your Free Trial
            </button>
          </motion.div>
        </section>
      </div>
    </div>
  )
}
