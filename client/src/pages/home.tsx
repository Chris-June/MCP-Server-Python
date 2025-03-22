import { Link } from 'react-router-dom'
import { motion } from 'framer-motion'
import { ArrowRight, Brain, MessageSquare, Users } from 'lucide-react'

import { Button } from '@/components/ui/button'

const features = [
  {
    icon: <Brain className="h-10 w-10 text-primary" />,
    title: 'Executive Advisory Team',
    description: 'Access a full suite of AI-powered executive advisors specializing in different business functions.',
  },
  {
    icon: <MessageSquare className="h-10 w-10 text-primary" />,
    title: 'Business Dashboard',
    description: 'Visualize key business metrics, advisor insights, and track progress towards your goals.',
  },
  {
    icon: <Users className="h-10 w-10 text-primary" />,
    title: 'Personalized Guidance',
    description: 'Receive tailored advice based on your specific business context and challenges.',
  },
]

export default function HomePage() {
  return (
    
    <div className="flex flex-col gap-12">
      <section className="text-center">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
          className="max-w-3xl mx-auto"
        >
          <h1 className="text-4xl md:text-5xl font-bold tracking-tight mb-6">
            Small Business
            <span className="text-primary"> Executive Advisors</span>
          </h1>
          <p className="text-xl text-muted-foreground mb-8">
            AI-powered executive guidance to help your small business thrive.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Button asChild size="lg">
              <Link to="/chat">
                Start Chatting <ArrowRight className="ml-2 h-4 w-4" />
              </Link>
            </Button>
            <Button asChild variant="outline" size="lg">
              <Link to="/roles">Explore Roles</Link>
            </Button>
          </div>
        </motion.div>
      </section>

      <section>
        <div className="text-center mb-12">
          <h2 className="text-3xl font-bold mb-4">Key Features</h2>
          <p className="text-muted-foreground max-w-2xl mx-auto">
            Our platform provides a powerful way to interact with specialized AI agents.
          </p>
        </div>

        <div className="grid md:grid-cols-3 gap-8">
          {features.map((feature, index) => (
            <motion.div
              key={index}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5, delay: index * 0.1 }}
              className="flex flex-col items-center text-center p-6 rounded-lg border bg-card"
            >
              <div className="mb-4">{feature.icon}</div>
              <h3 className="text-xl font-semibold mb-2">{feature.title}</h3>
              <p className="text-muted-foreground">{feature.description}</p>
            </motion.div>
          ))}
        </div>
      </section>

      <section className="bg-muted/30 -mx-4 px-4 py-12 rounded-lg">
        <div className="max-w-3xl mx-auto text-center">
          <h2 className="text-3xl font-bold mb-4">How It Works</h2>
          <p className="text-muted-foreground mb-8">
            The MCP (Model Context Protocol) Server orchestrates AI agents with role-specific context management.
          </p>
          
          <div className="flex flex-col gap-6">
            <div className="bg-background p-6 rounded-lg border">
              <h3 className="text-xl font-semibold mb-2">1. Choose a Role</h3>
              <p className="text-muted-foreground">
                Select from pre-defined roles like Marketing Expert, Financial Advisor, or create your own custom role.
              </p>
            </div>
            
            <div className="bg-background p-6 rounded-lg border">
              <h3 className="text-xl font-semibold mb-2">2. Ask Your Question</h3>
              <p className="text-muted-foreground">
                The AI agent will respond based on its specialized expertise, tone profile, and any contextual memories.
              </p>
            </div>
            
            <div className="bg-background p-6 rounded-lg border">
              <h3 className="text-xl font-semibold mb-2">3. Build Context Over Time</h3>
              <p className="text-muted-foreground">
                The system remembers important information, making future interactions more personalized and relevant.
              </p>
            </div>
          </div>
        </div>
      </section>
    </div>
  )
}
