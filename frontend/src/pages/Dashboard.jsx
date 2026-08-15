import { useEffect, useState } from 'react'
import api from '../services/api'

const StatCard = ({ label, value, icon, color }) => (
  <div className="bg-white rounded-lg shadow p-4">
    <div className="flex items-center justify-between">
      <div>
        <p className="text-sm text-gray-500">{label}</p>
        <p className="text-2xl font-bold mt-1">{value}</p>
      </div>
      <div className={`p-3 rounded-lg ${color}`}>{icon}</div>
    </div>
  </div>
)

export default function Dashboard() {
  const [data, setData] = useState(null)

  useEffect(() => {
    api.get('/reports/dashboard').then((res) => setData(res.data)).catch(console.error)
  }, [])

  if (!data) {
    return (
      <div className="flex items-center justify-center h-64 text-gray-500">Loading dashboard...</div>
    )
  }

  return (
    <div>
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
        <StatCard label="Total Orders" value={data.total_orders} color="bg-blue-100 text-blue-600" icon="📦" />
        <StatCard label="Open Orders" value={data.open_orders} color="bg-yellow-100 text-yellow-600" icon="📋" />
        <StatCard label="Styles" value={data.total_styles} color="bg-green-100 text-green-600" icon="👕" />
        <StatCard label="Buyers" value={data.total_buyers} color="bg-purple-100 text-purple-600" icon="🏢" />
        <StatCard label="Suppliers" value={data.total_suppliers} color="bg-indigo-100 text-indigo-600" icon="🚚" />
        <StatCard label="In Production" value={data.production_orders} color="bg-orange-100 text-orange-600" icon="🏭" />
        <StatCard label="Pending Shipments" value={data.pending_shipments} color="bg-red-100 text-red-600" icon="🚢" />
        <StatCard label="Overdue TNA" value={data.overdue_milestones} color="bg-pink-100 text-pink-600" icon="⏰" />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2 bg-white rounded-lg shadow p-4">
          <h2 className="text-lg font-semibold mb-4">Recent Orders</h2>
          <table className="w-full text-sm">
            <thead>
              <tr className="text-left text-gray-500 border-b">
                <th className="pb-2">PO Number</th>
                <th className="pb-2">Status</th>
                <th className="pb-2">Delivery Date</th>
                <th className="pb-2">Quantity</th>
              </tr>
            </thead>
            <tbody>
              {data.recent_orders?.map((order) => (
                <tr key={order.id} className="border-b last:border-0">
                  <td className="py-2">{order.po_number}</td>
                  <td className="py-2">
                    <span className="px-2 py-1 rounded-full bg-blue-100 text-blue-700 text-xs">
                      {order.status}
                    </span>
                  </td>
                  <td className="py-2">{order.delivery_date}</td>
                  <td className="py-2">{order.total_quantity}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
        <div className="bg-white rounded-lg shadow p-4">
          <h3 className="text-lg font-semibold mb-4">Inventory Summary</h3>
          <div className="space-y-4">
            <div>
              <div className="flex justify-between text-sm mb-1">
                <span className="text-gray-500">Raw Materials</span>
                <span className="font-medium">{data.raw_material_balance}</span>
              </div>
              <div className="w-full bg-gray-200 rounded-full h-2">
                <div className="bg-blue-600 h-2 rounded-full" style={{ width: '100%' }} />
              </div>
            </div>
            <div>
              <div className="flex justify-between text-sm mb-1">
                <span className="text-gray-500">WIP</span>
                <span className="font-medium">{data.wip_balance}</span>
              </div>
              <div className="w-full bg-gray-200 rounded-full h-2">
                <div className="bg-yellow-500 h-2 rounded-full" style={{ width: '100%' }} />
              </div>
            </div>
            <div>
              <div className="flex justify-between text-sm mb-1">
                <span className="text-gray-500">Finished Goods</span>
                <span className="font-medium">{data.finished_goods_balance}</span>
              </div>
              <div className="w-full bg-gray-200 rounded-full h-2">
                <div className="bg-green-500 h-2 rounded-full" style={{ width: '100%' }} />
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}