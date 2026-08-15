import { Routes, Route, Navigate } from 'react-router-dom'
import { useAuth } from './auth/AuthContext'
import Layout from './components/Layout'
import Login from './pages/Login'
import Dashboard from './pages/Dashboard'
import Buyers from './pages/Buyers'
import Suppliers from './pages/Suppliers'
import Styles from './pages/Styles'
import Materials from './pages/Materials'
import Colors from './pages/Colors'
import Sizes from './pages/Sizes'
import Orders from './pages/Orders'
import Boms from './pages/Boms'
import MaterialRequirements from './pages/MaterialRequirements'
import Inventory from './pages/Inventory'
import Requisitions from './pages/Requisitions'
import PurchaseOrders from './pages/PurchaseOrders'
import GoodsReceipts from './pages/GoodsReceipts'
import ProductionPlans from './pages/ProductionPlans'
import WorkOrders from './pages/WorkOrders'
import Cutting from './pages/Cutting'
import Sewing from './pages/Sewing'
import Finishing from './pages/Finishing'
import Quality from './pages/Quality'
import Packing from './pages/Packing'
import Shipments from './pages/Shipments'
import TNA from './pages/TNA'
import Reports from './pages/Reports'

function ProtectedRoute({ children }) {
  const { user } = useAuth()
  if (!user) return <Navigate to="/login" replace />
  return children
}

function App() {
  return (
    <Routes>
      <Route path="/login" element={<Login />} />
      <Route
        path="/"
        element={
          <ProtectedRoute>
            <Layout />
          </ProtectedRoute>
        }
      >
        <Route index element={<Dashboard />} />
        <Route path="buyers" element={<Buyers />} />
        <Route path="suppliers" element={<Suppliers />} />
        <Route path="styles" element={<Styles />} />
        <Route path="materials" element={<Materials />} />
        <Route path="colors" element={<Colors />} />
        <Route path="sizes" element={<Sizes />} />
        <Route path="orders" element={<Orders />} />
        <Route path="boms" element={<Boms />} />
        <Route path="material-requirements" element={<MaterialRequirements />} />
        <Route path="inventory" element={<Inventory />} />
        <Route path="requisitions" element={<Requisitions />} />
        <Route path="purchase-orders" element={<PurchaseOrders />} />
        <Route path="goods-receipts" element={<GoodsReceipts />} />
        <Route path="production-plans" element={<ProductionPlans />} />
        <Route path="work-orders" element={<WorkOrders />} />
        <Route path="cutting" element={<Cutting />} />
        <Route path="sewing" element={<Sewing />} />
        <Route path="finishing" element={<Finishing />} />
        <Route path="quality" element={<Quality />} />
        <Route path="packing" element={<Packing />} />
        <Route path="shipments" element={<Shipments />} />
        <Route path="tna" element={<TNA />} />
        <Route path="reports" element={<Reports />} />
      </Route>
    </Routes>
  )
}

export default App