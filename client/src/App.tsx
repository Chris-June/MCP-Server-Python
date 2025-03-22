import { Routes, Route } from 'react-router-dom'
import { Toaster } from '@/components/ui/toaster'
import { ThemeProvider } from '@/components/theme-provider'

import Layout from '@/components/layout'
import HomePage from '@/pages/home'
import RolesPage from '@/pages/roles'
import RoleDetailPage from '@/pages/role-detail'
import ChatPage from '@/pages/chat'
import DashboardPage from '@/pages/dashboard'

function App() {
  return (
    <ThemeProvider defaultTheme="system" storageKey="mcp-theme">
      <Toaster />
      <Routes>
        <Route path="/" element={<Layout />}>
          <Route index element={<HomePage />} />
          <Route path="dashboard" element={<DashboardPage />} />
          <Route path="roles" element={<RolesPage />} />
          <Route path="roles/:roleId" element={<RoleDetailPage />} />
          <Route path="chat" element={<ChatPage />} />
        </Route>
      </Routes>
    </ThemeProvider>
  )
}

export default App
