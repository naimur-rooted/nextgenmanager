import { useState } from 'react'
import { Outlet, NavLink, useNavigate } from 'react-router-dom'
import {
  LayoutDashboard,
  Users,
  Truck,
  Shirt,
  Boxes,
  Palette,
  Ruler,
  ShoppingCart,
  ClipboardCheck,
  Scissors,
  Stitch,
  Sparkles,
  ShieldCheck,
  Package,
  PackageCheck,
  Receipt,
  Ship,
  CalendarClock,
  BarChart3,
  LogOut,
} from 'lucide-react'
import { useAuth } from '../auth/AuthContext'

const navSections = [
  {
    title: 'Overview',
    items: [{ to: '/', label: 'Dashboard', icon: LayoutDashboard }],
  },
  {
    title: 'Master Data',
    items: [
      { to: '/buyers', label: 'Buyers', icon: Users },
      { to: '/suppliers', label: 'Suppliers', icon: Truck },
      { to: '/styles', label: 'Styles', icon: Shirt },
      { to: '/materials', label: 'Materials', icon: Boxes },
      { to: '/colors', label: 'Colors', icon: Palette },
      { to: '/sizes', label: 'Sizes', icon: Ruler },
    ],
  },
  {
    title: 'Merchandising',
    items: [
      { to: '/orders', label: 'Buyer Orders', icon: ShoppingCart },
      { to: '/tna', label: 'TNA', icon: CalendarClock },
    ],
  },
  {
    title: 'BOM',
    items: [
      { to: '/boms', label: 'BOM', icon: Package },
      { to: '/material-requirements', label: 'Material Requirements', icon: ClipboardCheck },
    ],
  },
  {
    title: 'Procurement',
    items: [
      { to: '/requisitions', label: 'Purchase Requisitions', icon: Receipt },
      { to: '/purchase-orders', label: 'Purchase Orders', icon: ShoppingCart },
      { to: '/goods-receipts', label: 'Goods Receipts', icon: Package },
    ],
  },
  {
    title: 'Inventory',
    items: [{ to: '/inventory', label: 'Inventory', icon: Boxes }],
  },
  {
    title: 'Production',
    items: [
      { to: '/production-plans', label: 'Production Plans', icon: CalendarClock },
      { to: '/cutting', label: 'Cutting', icon: Scissors },
      { to: '/sewing', label: 'Sewing', icon: Stitch },
      { to: '/finishing', label: 'Finishing', icon: Sparkles },
    ],
  },
  {
    title: 'Quality',
    items: [{ to: '/quality', label: 'Quality Control', icon: ShieldCheck }],
  },
  {
    title: 'Packing & Shipment',
    items: [
      { to: '/packing', label: 'Packing', icon: PackageCheck },
      { to: '/shipments', label: 'Shipments', icon: Ship },
    ],
  },
  {
    title: 'Analytics',
    items: [{ to: '/reports', label: 'Reports', icon: BarChart3 }],
  },
]

function Layout() {
  const navigate = useNavigate()
  const { user, logout } = useAuth()
  const [pageTitle, setPageTitle] = useState('Dashboard')

  const handleLogout = () => {
    logout()
    navigate('/login')
  }

  return (
    <div className="flex h-screen bg-gray-100">
      <aside className="w-64 bg-gray-900 text-gray-300 flex flex-col">
        <div className="p-4 border-b border-gray-800">
          <h1 className="text-lg font-bold text-white">NextGen ERP</h1>
          <p className="text-xs text-gray-500">Garment Manufacturing</p>
        </div>
        <nav className="flex-1 overflow-y-auto py-2">
          {navSections.map((section) => (
            <div key={section.title} className="mb-3">
              <div className="px-4 py-1 text-[11px] font-semibold uppercase tracking-wider text-gray-500">
                {section.title}
              </div>
              {section.items.map((item) => {
                const Icon = item.icon
                return (
                  <NavLink
                    key={item.to}
                    to={item.to}
                    onClick={() => setPageTitle(item.label)}
                    className={({ isActive }) =>
                      `flex items-center px-4 py-2 mx-2 rounded text-sm transition-colors ${
                        isActive
                          ? 'bg-blue-600 text-white'
                          : 'hover:bg-gray-800 hover:text-white'
                      }`
                    }
                  >
                    <Icon size={16} className="mr-3" />
                    {item.label}
                  </NavLink>
                )
              })}
            </div>
          ))}
        </nav>
        <div className="p-4 border-t border-gray-800">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-white">{user?.full_name}</p>
              <p className="text-xs text-gray-500">{user?.role}</p>
            </div>
            <button
              onClick={handleLogout}
              className="p-2 rounded hover:bg-gray-800 text-gray-400 hover:text-white"
            >
              <LogOut size={18} />
            </button>
          </div>
        </div>
      </aside>
      <div className="flex-1 flex flex-col overflow-hidden">
        <header className="h-14 bg-white border-b flex items-center px-6">
          <h1 className="text-lg font-semibold text-gray-800">{pageTitle}</h1>
        </header>
        <main className="flex-1 overflow-y-auto bg-gray-50">
          <div className="p-6">
            <Outlet />
          </div>
        </main>
      </div>
    </div>
  )
}

export default Layout