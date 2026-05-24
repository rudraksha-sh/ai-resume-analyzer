import {

  BrowserRouter,

  Routes,

  Route

} from "react-router-dom"

import Landing from "./pages/Landing"

import Dashboard from "./pages/Dashboard"

import RecruiterGPT from "./pages/RecruiterGPT"

function App() {

  return (

    <BrowserRouter>

      <Routes>

        <Route
          path="/"
          element={<Landing />}
        />

        <Route
          path="/dashboard"
          element={<Dashboard />}
        />

        <Route
          path="/chat"
          element={<RecruiterGPT />}
        />

      </Routes>

    </BrowserRouter>
  )
}

export default App