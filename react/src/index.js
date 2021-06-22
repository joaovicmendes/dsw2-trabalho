import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import './fonts.css';
import Helmet from 'react-helmet'


import Sidebar from './components/sidebar/sidebar'
import Topmenu from './components/topmenu/topmenu'
import Main from './components/main/main'



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
                </div>

            </div>
        </div>
    )
}

ReactDOM.render(
    <Page />,
    document.getElementById('root')
  );