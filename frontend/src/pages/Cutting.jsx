import { useEffect, useState } from 'react'
import api from '../services/api'
import DataTable from '../components/ui/DataTable'

export default function Cutting() {
  const [data, setData] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    setLoading(true)
    api.get('/production/cutting')
      .then((res) => setData(res.data))
      .catch(console.error)
      .finally(() => setLoading(false))
  }, [])

  const columns = [
    { key: 'work_order_id', label: 'WO ID' },
    { key: 'entry_date', label: 'Date' },
    { key: 'quantity', label: 'Garments Cut' },
    { key: 'rejection_qty', label: 'Rejection' },
    { key: 'operator', label: 'Operator' },
  ]

  return (
    <div>
      <DataTable columns={columns} data={data} loading={loading} searchPlaceholder="Search cutting entries..." />
    </div>
  )
}
