import { useEffect, useState } from 'react'
import api from '../services/api'
import DataTable from '../components/ui/DataTable'

export default function PurchaseOrders() {
  const [data, setData] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    setLoading(true)
    api.get('/purchase-orders')
      .then((res) => setData(res.data))
      .catch(console.error)
      .finally(() => setLoading(false))
  }, [])

  const columns = [
    { key: 'po_number', label: 'PO Number' },
    { key: 'supplier_id', label: 'Supplier ID' },
    { key: 'order_date', label: 'Order Date' },
    { key: 'expected_date', label: 'Expected Date' },
    { key: 'status', label: 'Status', render: (row) => row.status || 'Draft' },
  ]

  return (
    <div>
      <DataTable columns={columns} data={data} loading={loading} searchPlaceholder="Search purchase orders..." />
    </div>
  )
}
