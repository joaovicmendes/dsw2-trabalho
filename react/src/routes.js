import React from 'react';
import { BrowserRouter, Route, Switch } from 'react-router-dom';
import Sidebar from './components/sidebar'
import Topmenu from './components/topmenu'
import Main from './components/main'
import Page from './components/Page'
import Cadastro from './components/cadastro'
import CadastroSite from './components/cadastroSite'
import CadastroHotel from './components/cadastroHotel'

function Routes(){
    return(
        <BrowserRouter>
            <Sidebar/>
            <Topmenu/>
            <Main/>
            <Switch>
                <Route path='/' exact render={Page}/>
                <Route path='/login' exact render={Page}/>
                <Route path='/cadastrar/site' exact render={CadastroSite}/>
                <Route path='/cadastrar/hotel' exact render={CadastroHotel}/>
                <Route path='/cadastrar' exact render={Cadastro}/>
                <Route path='/hoteis' exact render={Page}/>
                <Route path='/sites' exact render={Page}/>
                <Route path='/cadastro/promocao' exact render={Page}/>

            </Switch>
        </BrowserRouter>
    )
}

export default Routes