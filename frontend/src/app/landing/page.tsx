'use client'

import { motion } from 'framer-motion'
import { useRouter } from 'next/navigation'
import { Sparkles, Zap, Target, Users, GitBranch, Presentation, ArrowRight, CheckCircle2 } from 'lucide-react'

export default function LandingPage() {
  const router = useRouter()

  const features = [
    {
      icon: Target,
      title: 'Idea Validation',
      description: 'Validate your hackathon idea against thousands of past projects using AI-powered search'
    },
    {
      icon: Sparkles,
      title: 'Contextual RAG',
      description: 'Get instant answers about hackathon rules, partner technologies, and best practices'
    },
    {
      icon: GitBranch,
      title: 'Progress Agent',
      description: 'Real-time tracking of your team\'s GitHub commits and project milestones'
    },
    {
      icon: Presentation,
      title: 'Presentation Assistant',
      description: 'Auto-generate pitch decks and demo scripts from your project documentation'
    }
  ]

  const stats = [
    { value: '10x', label: 'Faster Ideation' },
    { value: '50+', label: 'Hackathons Won' },
    { value: '100%', label: 'AI-Powered' },
    { value: '24/7', label: 'Team Support' }
  ]

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
          <div className="flex items-center space-x-4">
            <button
              onClick={() => router.push('/login')}
              className="px-6 py-2 text-white/80 hover:text-white transition-colors"
            >
              Login
            </button>
            <button
              onClick={() => router.push('/signup')}
              className="px-6 py-2 bg-white text-black rounded-lg hover:bg-white/90 transition-all glow-white font-medium"
            >
              Get Started
            </button>
          </div>
        </motion.nav>

        {/* Hero Section */}
        <section className="container mx-auto px-6 pt-20 pb-32">
          <div className="max-w-5xl mx-auto text-center">
            <motion.div
              initial={{ opacity: 0, y: 30 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.8, delay: 0.2 }}
            >
              <div className="inline-flex items-center space-x-2 px-4 py-2 bg-white/5 border border-white/10 rounded-full mb-8 glass">
                <Sparkles className="w-4 h-4 text-white" />
                <span className="text-sm text-white/80">Powered by Google Cloud & Elastic</span>
              </div>
            </motion.div>

            <motion.h1
              initial={{ opacity: 0, y: 30 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.8, delay: 0.3 }}
              className="text-6xl md:text-8xl font-bold mb-6 leading-tight"
            >
              Win Hackathons
              <br />
              <span className="shimmer">With AI Power</span>
            </motion.h1>

            <motion.p
              initial={{ opacity: 0, y: 30 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.8, delay: 0.4 }}
              className="text-xl md:text-2xl text-white/60 mb-12 max-w-3xl mx-auto"
            >
              Your AI-powered mentor that transforms how teams approach hackathons. 
              From ideation to presentation, we've got you covered.
            </motion.p>

            <motion.div
              initial={{ opacity: 0, y: 30 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.8, delay: 0.5 }}
              className="flex flex-col sm:flex-row items-center justify-center gap-4"
            >
              <button
                onClick={() => router.push('/signup')}
                className="group px-8 py-4 bg-white text-black rounded-lg hover:bg-white/90 transition-all glow-white font-semibold text-lg flex items-center space-x-2"
              >
                <span>Start Winning Now</span>
                <ArrowRight className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
              </button>
              <button
                onClick={() => router.push('/demo')}
                className="px-8 py-4 bg-white/5 border border-white/10 text-white rounded-lg hover:bg-white/10 transition-all glass font-semibold text-lg"
              >
                Watch Demo
              </button>
            </motion.div>
          </div>

          {/* Stats */}
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8, delay: 0.6 }}
            className="grid grid-cols-2 md:grid-cols-4 gap-8 max-w-4xl mx-auto mt-24"
          >
            {stats.map((stat, index) => (
              <div key={index} className="text-center">
                <div className="text-4xl md:text-5xl font-bold shimmer mb-2">{stat.value}</div>
                <div className="text-white/60">{stat.label}</div>
              </div>
            ))}
          </motion.div>
        </section>

        {/* Features Section */}
        <section className="container mx-auto px-6 py-32">
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
            viewport={{ once: true }}
            className="text-center mb-16"
          >
            <h2 className="text-4xl md:text-6xl font-bold mb-6">
              Everything You Need to <span className="shimmer">Win</span>
            </h2>
            <p className="text-xl text-white/60 max-w-2xl mx-auto">
              Powered by cutting-edge AI technology and designed for hackathon champions
            </p>
          </motion.div>

          <div className="grid md:grid-cols-2 gap-8 max-w-6xl mx-auto">
            {features.map((feature, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: 30 }}
                whileInView={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.6, delay: index * 0.1 }}
                viewport={{ once: true }}
                className="p-8 bg-white/5 border border-white/10 rounded-2xl glass hover:bg-white/10 transition-all group"
              >
                <div className="w-14 h-14 bg-white/10 rounded-xl flex items-center justify-center mb-6 group-hover:bg-white/20 transition-all">
                  <feature.icon className="w-7 h-7 text-white" />
                </div>
                <h3 className="text-2xl font-bold mb-4">{feature.title}</h3>
                <p className="text-white/60 text-lg">{feature.description}</p>
              </motion.div>
            ))}
          </div>
        </section>

        {/* How It Works */}
        <section className="container mx-auto px-6 py-32">
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
            viewport={{ once: true }}
            className="text-center mb-16"
          >
            <h2 className="text-4xl md:text-6xl font-bold mb-6">
              Simple. <span className="shimmer">Powerful.</span> Effective.
            </h2>
          </motion.div>

          <div className="max-w-4xl mx-auto space-y-8">
            {[
              { step: '01', title: 'Sign Up & Connect', description: 'Create your account and connect your GitHub repository' },
              { step: '02', title: 'Ask Anything', description: 'Get instant answers about rules, technologies, and best practices' },
              { step: '03', title: 'Track Progress', description: 'Monitor your team\'s commits and milestones in real-time' },
              { step: '04', title: 'Win Big', description: 'Auto-generate presentations and impress the judges' }
            ].map((item, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, x: -30 }}
                whileInView={{ opacity: 1, x: 0 }}
                transition={{ duration: 0.6, delay: index * 0.1 }}
                viewport={{ once: true }}
                className="flex items-start space-x-6 p-6 bg-white/5 border border-white/10 rounded-xl glass hover:bg-white/10 transition-all"
              >
                <div className="text-5xl font-bold text-white/20">{item.step}</div>
                <div className="flex-1">
                  <h3 className="text-2xl font-bold mb-2">{item.title}</h3>
                  <p className="text-white/60 text-lg">{item.description}</p>
                </div>
                <CheckCircle2 className="w-6 h-6 text-white/40" />
              </motion.div>
            ))}
          </div>
        </section>

        {/* CTA Section */}
        <section className="container mx-auto px-6 py-32">
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
            viewport={{ once: true }}
            className="max-w-4xl mx-auto text-center p-12 bg-white/5 border border-white/10 rounded-3xl glass"
          >
            <h2 className="text-4xl md:text-6xl font-bold mb-6">
              Ready to <span className="shimmer">Dominate</span> Your Next Hackathon?
            </h2>
            <p className="text-xl text-white/60 mb-8 max-w-2xl mx-auto">
              Join thousands of winning teams using AI to accelerate their hackathon success
            </p>
            <button
              onClick={() => router.push('/signup')}
              className="group px-10 py-5 bg-white text-black rounded-lg hover:bg-white/90 transition-all glow-white font-bold text-xl flex items-center space-x-2 mx-auto"
            >
              <span>Get Started Free</span>
              <ArrowRight className="w-6 h-6 group-hover:translate-x-1 transition-transform" />
            </button>
          </motion.div>
        </section>

        {/* Footer */}
        <footer className="container mx-auto px-6 py-12 border-t border-white/10">
          <div className="flex flex-col md:flex-row items-center justify-between">
            <div className="flex items-center space-x-2 mb-4 md:mb-0">
              <Zap className="w-6 h-6 text-white" />
              <span className="text-lg font-bold">Hackathon Agent</span>
            </div>
            <div className="text-white/60">
              Powered by Google Cloud & Elastic
            </div>
          </div>
        </footer>
      </div>
    </div>
  )
}
