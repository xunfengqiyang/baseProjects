import React from 'react';
import { Route } from 'react-router-dom';
import 'antd/dist/antd.css'
import './App.css';
import NavigationPage from './components/index'


const App = () => (
    <div className="app">
        <main>
            <Route exact path="/" component={ NavigationPage }/>
        </main>
    </div>

)


export default App;
