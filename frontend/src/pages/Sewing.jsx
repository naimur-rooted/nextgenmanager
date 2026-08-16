import { useEffect, useState } from 'react'
import api from '../services/api'
import DataTable from '../components/ui/DataTable'

export default function Sewing() {
  const [data, setData] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    setLoading(true)
    api.get('/sewing')
      .then((res) => setData(res.data))
      .catch((err) => {
        console.error('Failed to load sewing entries:', err)
        setData([])
      })
      .finally(() => setLoading(false))
  }, [])

  const totalSewn = data.reduce((acc, r) => acc + (r.quantity || 0), 0)
  const totalRejected = data.reduce((acc, r) => acc + (r.rejection_qty || 0), 0)

  const columns = [
    { key: 'wo_number', label: 'Work Order', render: (r) => <span className="font-semibold text-blue-900">{r.wo_number || `WO #${r.work_order_id}`}</span> },
    { key: 'entry_date', label: 'Sewing Date' },
    { key: 'quantity', label: 'Garments Sewn (Pcs)', render: (r) => <span className="font-bold text-gray-800">{r.quantity?.toLocaleString()}</span> },
    { key: 'rejection_qty', label: 'Sewing Rejection (Pcs)', render: (r) => <span className="text-red-600 font-semibold">{r.rejection_qty}</span> },
    { key: 'operator', label: 'Line / Supervisor' },
  ]

  return (
    <div className="space-y-4">
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="bg-white p-4 rounded-lg shadow-sm border border-gray-200">
          <p className="text-xs font-semibold text-gray-500 uppercase">Total Garments Sewn</p>
          <p className="text-2xl font-bold text-blue-700 mt-1">{totalSewn.toLocaleString()} Pcs</p>
          <p className="text-xs text-gray-500 mt-0.5">Sewing Line 01 Assembly</p>
        </div>
        <div className="bg-white p-4 rounded-lg shadow-sm border border-gray-200">
          <p className="text-xs font-semibold text-gray-500 uppercase">Line Alteration / Rejection</p>
          <p className="text-2xl font-bold text-red-600 mt-1">{totalRejected.toLocaleString()} Pcs</p>
          <p className="text-xs text-gray-500 mt-0.5">Stitch Defects / Skipped Stitches</p>
        </div>
        <div className="bg-white p-4 rounded-lg shadow-sm border border-gray-200">
          <p className="text-xs font-semibold text-gray-500 uppercase">Net Output for Finishing</p>
          <p className="text-2xl font-bold text-green-700 mt-1">{(totalSewn - totalRejected).toLocaleString()} Pcs</p>
          <p className="text-xs text-gray-500 mt-0.5">Transferred to Ironing & Packing</p>
        </div>
      </div>

      <DataTable columns={columns} data={data} loading={loading} searchPlaceholder="Search sewing logs..." />
    </div>
  )
}
