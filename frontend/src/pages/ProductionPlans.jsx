import { useEffect, useState } from 'react'
import api from '../services/api'
import DataTable from '../components/ui/DataTable'

export default function ProductionPlans() {
  const [plans, setPlans] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    setLoading(true)
    api.get('/production-plans')
      .then((res) => setPlans(res.data))
      .catch(console.error)
      .finally(() => setLoading(false))
  }, [])

  const columns = [
    { key: 'plan_number', label: 'Plan Number' },
    { key: 'order_id', label: 'Order ID' },
    { key: 'start_date', label: 'Start Date' },
    { key: 'end_date', label: 'End Date' },
    { key: 'status', label: 'Status', render: (row) => row.status || 'Draft' },
    { key: 'work_orders', label: 'WOs', render: (row) => row.work_orders?.length || 0 },
  ]

  return (
    <div>
      <DataTable columns={columns} data={plans} loading={loading} searchPlaceholder="Search production plans..." />
    </div>
  )
}
