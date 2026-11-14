import React from 'react'
import './App.css'
import Home from './component/Home'
import Analysis from './component/Analysis'
import Evaluation from './component/Evaluation'
import { BrowserRouter,Routes,Route } from 'react-router-dom'
function App() {


  return (
   <BrowserRouter>
   <Routes>
    <Route path='/' element={<Home/>}/>
    <Route path='/analysis' element={<Analysis/>}/>
    <Route path='/evaluation' element={<Evaluation/>}/>
   </Routes>
   </BrowserRouter>
  )
}

export default App
