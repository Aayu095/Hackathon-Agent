import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import './globals.css'

const inter = Inter({ subsets: ['latin'] })

export const metadata: Metadata = {
  title: '🤖 Hackathon Agent - AI-Powered Team Assistant',
  description: 'Transform your hackathon experience with AI-powered idea validation, progress tracking, and presentation assistance.',
  keywords: ['hackathon', 'AI', 'assistant', 'team', 'collaboration', 'Google Cloud', 'Elastic'],
  authors: [{ name: 'Hackathon Agent Team' }],
  openGraph: {
    title: '🤖 Hackathon Agent',
    description: 'AI-Powered Hackathon Team Assistant',
    type: 'website',
  },
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en" className="h-full dark">
      <body className={`${inter.className} h-full bg-black`}>
        <div className="min-h-full">
          {children}
        </div>
      </body>
    </html>
  )
}
