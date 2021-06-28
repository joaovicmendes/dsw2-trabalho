import React from 'react';
import { BrowserRouter, Route, Switch } from 'react-router-dom';
import Sidebar from './components/sidebar'
import Topmenu from './components/topmenu'
import Main from './components/main'
import Page from './components/Page'

function Routes(){
    return(
        <BrowserRouter>
            <Sidebar/>
            <Topmenu/>
            <Main/>
            <Switch>
                <Route path='/' render={Page}/>
                <Route path='/login' exact render={Page}/>
                <Route path='/cadastro' exact render={Page}/>
                <Route path='/hoteis' exact render={Page}/>
                <Route path='/sites' exact render={Page}/>
                <Route path='/cadastro/promocao' exact render={Page}/>

            </Switch>
        </BrowserRouter>
    )
}

export default Routes