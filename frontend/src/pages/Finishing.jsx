import { useEffect, useState } from 'react'
import api from '../services/api'
import DataTable from '../components/ui/DataTable'

export default function Finishing() {
  const [data, setData] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    setLoading(true)
    api.get('/finishing')
      .then((res) => setData(res.data))
      .catch((err) => {
        console.error('Failed to load finishing entries:', err)
        setData([])
      })
      .finally(() => setLoading(false))
  }, [])

  const totalFinished = data.reduce((acc, r) => acc + (r.quantity || 0), 0)
  const totalRejected = data.reduce((acc, r) => acc + (r.rejection_qty || 0), 0)

  const columns = [
    { key: 'wo_number', label: 'Work Order', render: (r) => <span className="font-semibold text-blue-900">{r.wo_number || `WO #${r.work_order_id}`}</span> },
    { key: 'entry_date', label: 'Finishing Date' },
    { key: 'quantity', label: 'Finished Garments (Pcs)', render: (r) => <span className="font-bold text-gray-800">{r.quantity?.toLocaleString()}</span> },
    { key: 'rejection_qty', label: 'Finishing Rejection (Pcs)', render: (r) => <span className="text-red-600 font-semibold">{r.rejection_qty}</span> },
    { key: 'operator', label: 'Section / Supervisor' },
  ]

  return (
    <div className="space-y-4">
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="bg-white p-4 rounded-lg shadow-sm border border-gray-200">
          <p className="text-xs font-semibold text-gray-500 uppercase">Total Finished Garments</p>
          <p className="text-2xl font-bold text-blue-700 mt-1">{totalFinished.toLocaleString()} Pcs</p>
          <p className="text-xs text-gray-500 mt-0.5">Ironed, Folded & Tagged</p>
        </div>
        <div className="bg-white p-4 rounded-lg shadow-sm border border-gray-200">
          <p className="text-xs font-semibold text-gray-500 uppercase">Finishing Rejection / Stain</p>
          <p className="text-2xl font-bold text-red-600 mt-1">{totalRejected.toLocaleString()} Pcs</p>
          <p className="text-xs text-gray-500 mt-0.5">Iron Burn / Fabric Stain</p>
        </div>
        <div className="bg-white p-4 rounded-lg shadow-sm border border-gray-200">
          <p className="text-xs font-semibold text-gray-500 uppercase">Passed for Quality Audit</p>
          <p className="text-2xl font-bold text-green-700 mt-1">{(totalFinished - totalRejected).toLocaleString()} Pcs</p>
          <p className="text-xs text-gray-500 mt-0.5">Ready for Final AQL Inspection</p>
        </div>
      </div>

      <DataTable columns={columns} data={data} loading={loading} searchPlaceholder="Search finishing logs..." />
    </div>
  )
}
