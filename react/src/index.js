import React from 'react';
import ReactDOM from 'react-dom';
import App from './app';

ReactDOM.render(
    <React.StrictMode>
      <App />
    </React.StrictMode>,
    document.getElementById('root'),
  );
  

/*

import './index.css';
import './fonts.css';
import './routes'
import Helmet from 'react-helmet'


import Sidebar from './components/sidebar/sidebar'
import Topmenu from './components/topmenu/topmenu'
import Main from './components/main/main'
import Table from './components/table/table'

export const Page = () => {

    return (
        
        <div>
            <Helmet>
                <meta charset="UTF-8"/>
                <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
                <title>Otelo</title>
                <link rel="icon" href="/static/Otelo.svg"/>
            </Helmet>
            <div class="main_body">
                <Sidebar/>
                <div class='wrapper'>
                    <Topmenu/>
                    <Main/>
                    <Table/>

                </div>

            </div>
        </div>
    )
}
*/
