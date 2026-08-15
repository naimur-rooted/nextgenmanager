import { useEffect, useState } from 'react'
import api from '../services/api'
import DataTable from '../components/ui/DataTable'

export default function Inventory() {
  const [balances, setBalances] = useState([])
  const [transactions, setTransactions] = useState([])
  const [view, setView] = useState('balances')
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    setLoading(true)
    const url = view === 'balances' ? '/inventory/balances' : '/inventory/transactions'
    api.get(url).then((res) => (view === 'balances' ? setBalances(res.data) : setTransactions(res.data)))
      .catch(console.error)
      .finally(() => setLoading(false))
  }, [view])

  const balanceColumns = [
    { key: 'material_code', label: 'Code' },
    { key: 'material_name', label: 'Material' },
    { key: 'category', label: 'Category' },
    { key: 'quantity', label: 'Quantity', render: (row) => <span className="font-medium">{row.quantity}</span> },
    { key: 'reserved_qty', label: 'Reserved' },
  ]

  const txColumns = [
    { key: 'transaction_date', label: 'Date', render: (row) => new Date(row.transaction_date).toLocaleDateString() },
    { key: 'transaction_type', label: 'Type' },
    { key: 'material_code', label: 'Code' },
    { key: 'material_name', label: 'Material' },
    {
      key: 'quantity',
      label: 'Qty (+/-)',
      render: (row) => (
        <span className={row.quantity > 0 ? 'text-green-600 font-medium' : 'text-red-600 font-medium'}>
          {row.quantity > 0 ? `+${row.quantity}` : row.quantity}
        </span>
      ),
    },
    { key: 'balance_after', label: 'Balance' },
    { key: 'remarks', label: 'Remarks' },
  ]

  return (
    <div>
      <div className="mb-4 inline-flex rounded-md shadow-sm" role="group">
        <button
          onClick={() => setView('balances')}
          className={`px-4 py-2 text-sm font-medium rounded-l-md border ${view === 'balances' ? 'bg-blue-600 text-white border-blue-600' : 'bg-white text-gray-700 border-gray-300'}`}
        >
          Balances
        </button>
        <button
          onClick={() => setView('transactions')}
          className={`px-4 py-2 text-sm font-medium rounded-r-md border ${view === 'transactions' ? 'bg-blue-600 text-white border-blue-600' : 'bg-white text-gray-700 border-gray-300'}`}
        >
          Transactions
        </button>
      </div>
      {view === 'balances' ? (
        <DataTable columns={balanceColumns} data={balances} loading={loading} searchPlaceholder="Search stock..." />
      ) : (
        <DataTable columns={txColumns} data={transactions} loading={loading} searchPlaceholder="Search transactions..." />
      )}
    </div>
  )
}