import { useEffect, useState } from 'react'
import api from '../services/api'
import DataTable from '../components/ui/DataTable'

export default function GoodsReceipts() {
  const [data, setData] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    setLoading(true)
    api.get('/goods-receipts')
      .then((res) => setData(res.data))
      .catch(console.error)
      .finally(() => setLoading(false))
  }, [])

  const columns = [
    { key: 'gr_number', label: 'GR Number' },
    { key: 'purchase_order_id', label: 'PO ID' },
    { key: 'receipt_date', label: 'Receipt Date' },
    { key: 'received_by', label: 'Received By' },
    { key: 'status', label: 'Status', render: (row) => row.status || 'Draft' },
  ]

  return (
    <div>
      <DataTable columns={columns} data={data} loading={loading} searchPlaceholder="Search goods receipts..." />
    </div>
  )
}
