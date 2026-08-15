import { useEffect, useState } from 'react'
import api from '../services/api'
import DataTable from '../components/ui/DataTable'

export default function WorkOrders() {
  const [data, setData] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    setLoading(true)
    api.get('/work-orders')
      .then((res) => setData(res.data))
      .catch(console.error)
      .finally(() => setLoading(false))
  }, [])

  const columns = [
    { key: 'wo_number', label: 'WO Number' },
    { key: 'plan_id', label: 'Plan ID' },
    { key: 'quantity', label: 'Quantity' },
    { key: 'produced_qty', label: 'Produced Qty' },
    { key: 'rejected_qty', label: 'Rejected Qty' },
    { key: 'status', label: 'Status', render: (row) => row.status || 'Planned' },
  ]

  return (
    <div>
      <DataTable columns={columns} data={data} loading={loading} searchPlaceholder="Search work orders..." />
    </div>
  )
}
