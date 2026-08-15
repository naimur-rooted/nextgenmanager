import { useEffect, useState } from 'react'
import api from '../services/api'
import DataTable from '../components/ui/DataTable'
import Modal from '../components/ui/Modal'

export default function TNA() {
  const [milestones, setMilestones] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    setLoading(true)
    api.get('/tna/milestones').then((res) => setMilestones(res.data)).catch(console.error).finally(() => setLoading(false))
  }, [])

  const columns = [
    { key: 'milestone_name', label: 'Milestone' },
    { key: 'target_date', label: 'Target Date', render: (row) => new Date(row.target_date).toLocaleDateString() },
    { key: 'status', label: 'Status', render: (row) => (row.status ? row.status : 'Pending') },
    { key: 'order_qty', label: 'Order Qty' },
    { key: 'completed_qty', label: 'Completed' },
    {
      key: 'completion_percent',
      label: '% Complete',
      render: (row) => (
        <div className="flex items-center gap-2">
          <span className="text-sm">{row.completion_percent}%</span>
          <div className="w-32 h-2 bg-gray-200 rounded-full overflow-hidden">
            <div className={`h-2 rounded-full ${row.completion_percent > 50 ? 'bg-green-600' : 'bg-blue-500'} rounded-full transition-colors`} style={{ width: `${row.completion_percent}%` }} />
          </div>
        </div>
      ),
    },
  ]

  return (
    <div>
      <DataTable columns={columns} data={milestones} loading={loading} searchPlaceholder="Search milestones..." />
    </div>
  )
}