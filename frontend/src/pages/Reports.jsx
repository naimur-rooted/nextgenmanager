import { useEffect, useState } from 'react'
import api from '../services/api'

export default function Reports() {
  const [data, setData] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    setLoading(true)
    api.get('/reports/summary')
      .then((res) => setData(res.data))
      .catch(console.error)
      .finally(() => setLoading(false))
  }, [])

  if (loading) return <div className="p-4 text-gray-500">Loading summary report...</div>

  return (
    <div className="space-y-6">
      <h2 className="text-xl font-bold text-gray-800">Executive Summary Report</h2>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="bg-white p-4 rounded shadow border">
          <p className="text-xs font-semibold text-gray-500 uppercase">Total Orders</p>
          <p className="text-2xl font-bold text-gray-800">{data?.total_orders ?? 0}</p>
        </div>
        <div className="bg-white p-4 rounded shadow border">
          <p className="text-xs font-semibold text-gray-500 uppercase">Open Orders</p>
          <p className="text-2xl font-bold text-blue-600">{data?.open_orders ?? 0}</p>
        </div>
        <div className="bg-white p-4 rounded shadow border">
          <p className="text-xs font-semibold text-gray-500 uppercase">Active Styles</p>
          <p className="text-2xl font-bold text-green-600">{data?.total_styles ?? 0}</p>
        </div>
      </div>
    </div>
  )
}
