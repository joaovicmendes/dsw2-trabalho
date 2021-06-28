import React from 'react';
import { BrowserRouter, Route, Switch } from 'react-router-dom';
import Sidebar from './components/sidebar'
import Topmenu from './components/topmenu'
import Main from './components/main'
import Page from './components/page'

import Table from './components/table'
import Login from './components/login'

import Cadastro from './components/cadastro'
import CadastroSite from './components/cadastroSite'
import CadastroHotel from './components/cadastroHotel'



function Routes(){
    return(
        <BrowserRouter>

            <div className="main_body">
            {/* <Sidebar/> */}
                <div className='wrapper'>
                    <Topmenu/>
                    {/* <Main/> */}
                    <Switch>
                        <Route path='/' exact render={Table}/>
                        <Route path='/login' exact render={Login}/>
                        <Route path='/cadastrar/site' exact render={CadastroSite}/>
                        <Route path='/cadastrar/hotel' exact render={CadastroHotel}/>
                        <Route path='/cadastrar' exact render={Cadastro}/>
                        <Route path='/hoteis' exact render={Table}/>
                        <Route path='/sites' exact render={Table}/>
                        <Route path='/cadastrar/promocao' exact render={Page}/>
                    </Switch>
                </div>
            </div>
        </BrowserRouter>
    )
}

export default Routes