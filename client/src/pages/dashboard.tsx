import { useState } from 'react';
import { motion } from 'framer-motion';
import { ArrowUpRight, BarChart3, DollarSign, TrendingUp, Users, PieChart } from 'lucide-react';

import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from '@/components/ui/card';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Button } from '@/components/ui/button';

interface MetricCardProps {
  title: string;
  value: string;
  description: string;
  icon: React.ReactNode;
  trend?: number;
  trendLabel?: string;
}

const MetricCard = ({ title, value, description, icon, trend, trendLabel }: MetricCardProps) => {
  return (
    <Card>
      <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
        <CardTitle className="text-sm font-medium">{title}</CardTitle>
        <div className="h-4 w-4 text-muted-foreground">{icon}</div>
      </CardHeader>
      <CardContent>
        <div className="text-2xl font-bold">{value}</div>
        <p className="text-xs text-muted-foreground">{description}</p>
      </CardContent>
      {trend !== undefined && (
        <CardFooter className="p-2">
          <div className={`flex items-center text-xs ${trend >= 0 ? 'text-green-500' : 'text-red-500'}`}>
            {trend >= 0 ? '+' : ''}{trend}% {trendLabel}
            <ArrowUpRight className={`ml-1 h-3 w-3 ${trend < 0 ? 'rotate-180 transform' : ''}`} />
          </div>
        </CardFooter>
      )}
    </Card>
  );
};

interface AdvisorInsightProps {
  advisor: string;
  title: string;
  content: string;
  date: string;
}

const AdvisorInsight = ({ advisor, title, content, date }: AdvisorInsightProps) => {
  return (
    <Card className="mb-4">
      <CardHeader className="pb-2">
        <div className="flex justify-between items-center">
          <CardTitle className="text-md font-medium">{title}</CardTitle>
          <span className="text-xs text-muted-foreground">{date}</span>
        </div>
        <CardDescription className="text-sm font-semibold text-primary">{advisor}</CardDescription>
      </CardHeader>
      <CardContent>
        <p className="text-sm">{content}</p>
      </CardContent>
      <CardFooter className="pt-1">
        <Button variant="ghost" size="sm" className="ml-auto">
          View Full Insight
        </Button>
      </CardFooter>
    </Card>
  );
};

export default function DashboardPage() {
  const [activeTab, setActiveTab] = useState('overview');

  // Sample data - in a real application, this would come from an API
  const businessMetrics = {
    revenue: { value: '$24,563', trend: 12.5, description: 'Monthly revenue' },
    customers: { value: '573', trend: 8.2, description: 'Total customers' },
    conversion: { value: '3.6%', trend: -1.1, description: 'Conversion rate' },
    expenses: { value: '$18,230', trend: 4.3, description: 'Monthly expenses' },
  };

  const recentInsights = [
    {
      advisor: 'CEO Advisor',
      title: 'Strategic Growth Opportunity',
      content: 'Based on your current market position and customer acquisition rate, expanding into the B2B sector could yield a 15-20% revenue increase within 6 months.',
      date: 'Today'
    },
    {
      advisor: 'CFO Advisor',
      title: 'Cash Flow Optimization',
      content: 'Your accounts receivable turnover has decreased by 8% this quarter. Consider implementing a new invoicing system to improve collection efficiency.',
      date: 'Yesterday'
    },
    {
      advisor: 'CMO Advisor',
      title: 'Marketing Channel Analysis',
      content: 'Social media campaigns are outperforming email marketing by 3:1 in terms of ROI. Recommend reallocating 20% of email budget to Instagram and LinkedIn.',
      date: '3 days ago'
    },
  ];

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
      className="space-y-6"
    >
      <div className="flex justify-between items-center">
        <h1 className="text-3xl font-bold tracking-tight">Business Dashboard</h1>
        <Button>Export Report</Button>
      </div>

      <Tabs defaultValue="overview" className="space-y-4" onValueChange={setActiveTab}>
        <TabsList>
          <TabsTrigger value="overview">Overview</TabsTrigger>
          <TabsTrigger value="insights">Advisor Insights</TabsTrigger>
          <TabsTrigger value="goals">Business Goals</TabsTrigger>
        </TabsList>

        <TabsContent value="overview" className="space-y-4">
          <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
            <MetricCard
              title="Revenue"
              value={businessMetrics.revenue.value}
              description={businessMetrics.revenue.description}
              icon={<DollarSign className="h-4 w-4" />}
              trend={businessMetrics.revenue.trend}
              trendLabel="from last month"
            />
            <MetricCard
              title="Customers"
              value={businessMetrics.customers.value}
              description={businessMetrics.customers.description}
              icon={<Users className="h-4 w-4" />}
              trend={businessMetrics.customers.trend}
              trendLabel="new customers"
            />
            <MetricCard
              title="Conversion Rate"
              value={businessMetrics.conversion.value}
              description={businessMetrics.conversion.description}
              icon={<BarChart3 className="h-4 w-4" />}
              trend={businessMetrics.conversion.trend}
              trendLabel="from last month"
            />
            <MetricCard
              title="Expenses"
              value={businessMetrics.expenses.value}
              description={businessMetrics.expenses.description}
              icon={<TrendingUp className="h-4 w-4" />}
              trend={businessMetrics.expenses.trend}
              trendLabel="from last month"
            />
          </div>

          <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-7">
            <Card className="col-span-4">
              <CardHeader>
                <CardTitle>Revenue Overview</CardTitle>
              </CardHeader>
              <CardContent className="pl-2">
                <div className="h-[200px] flex items-center justify-center">
                  <div className="text-muted-foreground flex flex-col items-center">
                    <BarChart3 className="h-16 w-16 mb-2 opacity-20" />
                    <p>Revenue chart will appear here</p>
                    <p className="text-xs">Connect your financial data to see insights</p>
                  </div>
                </div>
              </CardContent>
            </Card>
            <Card className="col-span-3">
              <CardHeader>
                <CardTitle>Expense Breakdown</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="h-[200px] flex items-center justify-center">
                  <div className="text-muted-foreground flex flex-col items-center">
                    <PieChart className="h-16 w-16 mb-2 opacity-20" />
                    <p>Expense chart will appear here</p>
                    <p className="text-xs">Connect your financial data to see insights</p>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>
        </TabsContent>

        <TabsContent value="insights" className="space-y-4">
          <div className="grid gap-4 md:grid-cols-1 lg:grid-cols-2">
            <div>
              <h2 className="text-xl font-semibold mb-4">Recent Advisor Insights</h2>
              {recentInsights.map((insight, index) => (
                <AdvisorInsight
                  key={index}
                  advisor={insight.advisor}
                  title={insight.title}
                  content={insight.content}
                  date={insight.date}
                />
              ))}
            </div>
            <Card>
              <CardHeader>
                <CardTitle>Request Business Analysis</CardTitle>
                <CardDescription>
                  Get a comprehensive analysis from our executive advisors based on your business data.
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  <div className="grid grid-cols-2 gap-4">
                    <Button variant="outline" className="h-24 flex flex-col">
                      <DollarSign className="h-8 w-8 mb-2" />
                      Financial Analysis
                    </Button>
                    <Button variant="outline" className="h-24 flex flex-col">
                      <Users className="h-8 w-8 mb-2" />
                      Customer Analysis
                    </Button>
                    <Button variant="outline" className="h-24 flex flex-col">
                      <BarChart3 className="h-8 w-8 mb-2" />
                      Market Analysis
                    </Button>
                    <Button variant="outline" className="h-24 flex flex-col">
                      <TrendingUp className="h-8 w-8 mb-2" />
                      Growth Strategy
                    </Button>
                  </div>
                </div>
              </CardContent>
              <CardFooter>
                <Button className="w-full">Request Custom Analysis</Button>
              </CardFooter>
            </Card>
          </div>
        </TabsContent>

        <TabsContent value="goals" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>Business Goals</CardTitle>
              <CardDescription>
                Track your progress towards important business milestones.
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="h-[300px] flex items-center justify-center">
                <div className="text-muted-foreground flex flex-col items-center">
                  <p>Set up your business goals to track progress</p>
                  <Button className="mt-4">Define Business Goals</Button>
                </div>
              </div>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </motion.div>
  );
}
