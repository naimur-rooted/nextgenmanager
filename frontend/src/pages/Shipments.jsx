import { useEffect, useState } from 'react'
import api from '../services/api'
import DataTable from '../components/ui/DataTable'

export default function Shipments() {
  const [data, setData] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    setLoading(true)
    api.get('/shipments').then((res) => setData(res.data)).catch(console.error).finally(() => setLoading(false))
  }, [])

  const columns = [
    { key: 'shipment_number', label: 'Shipment #', render: (row) => row.shipment_number },
    { key: 'po_number', label: 'PO' },
    { key: 'shipment_date', label: 'Date', render: (row) => new Date(row.shipment_date).toLocaleDateString() },
    { key: 'carrier', label: 'Carrier' },
    { key: 'status', label: 'Status', render: (row) => (row.status ? row.status : 'Planned') },
    { key: 'items_count', label: 'Items', render: (row) => row.items?.length || 0 },
  ]

  return (
    <div>
      <DataTable columns={columns} data={data} loading={loading} searchPlaceholder="Search shipments..." />
    </div>
  )
}