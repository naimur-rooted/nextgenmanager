import { useEffect, useState } from 'react'
import api from '../services/api'
import DataTable from '../components/ui/DataTable'

export default function Finishing() {
  const [data, setData] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    setLoading(true)
    api.get('/production/finishing')
      .then((res) => setData(res.data))
      .catch(console.error)
      .finally(() => setLoading(false))
  }, [])

  const columns = [
    { key: 'work_order_id', label: 'WO ID' },
    { key: 'entry_date', label: 'Date' },
    { key: 'quantity', label: 'Finished Qty' },
    { key: 'rejection_qty', label: 'Rejection' },
    { key: 'operator', label: 'Operator' },
  ]

  return (
    <div>
      <DataTable columns={columns} data={data} loading={loading} searchPlaceholder="Search finishing entries..." />
    </div>
  )
}
