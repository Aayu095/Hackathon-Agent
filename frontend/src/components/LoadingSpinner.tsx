import { motion } from 'framer-motion'
import { Zap } from 'lucide-react'

export function LoadingSpinner() {
  return (
    <div className="flex items-center justify-center">
      <motion.div
        animate={{ rotate: 360 }}
        transition={{ duration: 1, repeat: Infinity, ease: 'linear' }}
      >
        <Zap className="w-8 h-8 text-white" />
      </motion.div>
    </div>
  )
}
