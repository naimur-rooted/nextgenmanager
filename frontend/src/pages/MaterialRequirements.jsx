import { useEffect, useState } from 'react'
import api from '../services/api'
import DataTable from '../components/ui/DataTable'

export default function MaterialRequirements() {
  const [data, setData] = useState([])
  const [orders, setOrders] = useState([])
  const [loading, setLoading] = useState(true)

  const load = () => {
    setLoading(true)
    api.get('/material-requirements').then((res) => setData(res.data)).catch(console.error).finally(() => setLoading(false))
    api.get('/orders').then((res) => setOrders(res.data)).catch(console.error)
  }

  useEffect(load, [])

  const calculateForOrder = async (orderId) => {
    await api.post(`/material-requirements/calculate/${orderId}`)
    load()
  }

  const columns = [
    { key: 'po_number', label: 'PO Number' },
    { key: 'material_code', label: 'Material Code' },
    { key: 'material_name', label: 'Material' },
    { key: 'total_order_qty', label: 'Order Qty' },
    { key: 'consumption_per_unit', label: 'Per Unit' },
    { key: 'wastage_percent', label: 'Wastage %' },
    {
      key: 'required_qty',
      label: 'Required',
      render: (row) => <span className="font-medium">{row.required_qty}</span>,
    },
    {
      key: 'available_qty',
      label: 'Available',
      render: (row) => <span className="text-blue-600">{row.available_qty}</span>,
    },
    {
      key: 'incoming_qty',
      label: 'Incoming',
      render: (row) => <span className="text-yellow-600">{row.incoming_qty}</span>,
    },
    {
      key: 'shortage_qty',
      label: 'Shortage',
      render: (row) => (
        <span className={row.shortage_qty > 0 ? 'text-red-600 font-medium' : 'text-green-600'}>
          {row.shortage_qty}
        </span>
      ),
    },
  ]

  return (
    <div>
      <div className="mb-4 flex items-center gap-2">
        <select className="input max-w-xs" onChange={(e) => e.target.value && calculateForOrder(e.target.value)}>
          <option value="">Select order to calculate...</option>
          {orders.map((o) => <option key={o.id} value={o.id}>{o.po_number}</option>)}
        </select>
      </div>
      <DataTable columns={columns} data={data} loading={loading} searchPlaceholder="Search requirements..." />
    </div>
  )
}