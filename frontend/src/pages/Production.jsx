import { useEffect, useState } from 'react'
import api from '../services/api'
import DataTable from '../components/ui/DataTable'

export default function Production() {
  const [plans, setPlans] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    setLoading(true)
    api.get('/production-plans').then((res) => setPlans(res.data)).catch(console.error).finally(() => setLoading(false))
  }, [])

  const columns = [
    { key: 'plan_number', label: 'Plan Number' },
    { key: 'po_number', label: 'PO' },
    { key: 'start_date', label: 'Start' },
    { key: 'end_date', label: 'End' },
    { key: 'status', label: 'Status', render: (row) => (row.status ? row.status : 'Draft') },
    { key: 'work_orders', label: 'WOs', render: (row) => row.work_orders?.length || 0 },
  ]

  return (
    <div>
      <DataTable columns={columns} data={plans} loading={loading} searchPlaceholder="Search plans..." />
    </div>
  )
}