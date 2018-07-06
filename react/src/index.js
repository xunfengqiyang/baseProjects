import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import App from './App';
import { Provider } from 'react-redux';
import { ConnectedRouter } from 'react-router-redux';
import store, { history } from './store';
//import registerServiceWorker from './registerServiceWorker';


ReactDOM.render(
	<Provider store={store}>
	    <ConnectedRouter history={history}>
				<div style={{height: "100%"}}>
					<App />
				</div>
	    </ConnectedRouter>
  	</Provider>, document.getElementById('root'));

// registerServiceWorker();
