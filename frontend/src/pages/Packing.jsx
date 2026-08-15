import { useEffect, useState } from 'react'
import api from '../services/api'
import DataTable from '../components/ui/DataTable'
import Modal from '../components/ui/Modal'

export default function Packing() {
  const [lists, setLists] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    setLoading(true)
    api.get('/packing/lists').then((res) => setLists(res.data)).catch(console.error).finally(() => setLoading(false))
  }, [])

  const columns = [
    { key: 'packing_number', label: 'Packing #', render: (row) => row.packing_number },
    { key: 'po_number', label: 'PO' },
    { key: 'status', label: 'Status', render: (row) => (row.status ? row.status : 'Draft') },
    { key: 'total_quantity', label: 'Qty' },
    { key: 'warehouse', label: 'Warehouse' },
  ]

  return (
    <div>
      <DataTable columns={columns} data={lists} loading={loading} searchPlaceholder="Search packing lists..." />
    </div>
  )
}