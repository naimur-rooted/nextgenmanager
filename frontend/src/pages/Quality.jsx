import { useEffect, useState } from 'react'
import api from '../services/api'
import DataTable from '../components/ui/DataTable'
import Modal from '../components/ui/Modal'

export default function Quality() {
  const [inspections, setInspections] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    setLoading(true)
    api.get('/quality/inspections').then((res) => setInspections(res.data)).catch(console.error).finally(() => setLoading(false))
  }, [])

  const columns = [
    { key: 'inspection_number', label: 'Inspection #' },
    { key: 'qc_type', label: 'Type' },
    { key: 'status', label: 'Status', render: (row) => (row.status ? row.status : 'Pending') },
    { key: 'inspected_qty', label: 'Inspected' },
    { key: 'passed_qty', label: 'Passed' },
    { key: 'rejected_qty', label: 'Rejected' },
    { key: 'inspector', label: 'Inspector' },
    { key: 'inspection_date', label: 'Date', render: (row) => new Date(row.inspection_date).toLocaleDateString() },
  ]

  return (
    <div>
      <DataTable columns={columns} data={inspections} loading={loading} searchPlaceholder="Search inspections..." />
    </div>
  )
}