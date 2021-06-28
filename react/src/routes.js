import React from 'react';
import { BrowserRouter, Redirect, Route, Switch } from 'react-router-dom';
import Sidebar from './components/Sidebar/Sidebar'
import Topmenu from './components/Topmenu/Topmenu'
import Main from './components/Main/Main'
import Page from './components/Page/Page'
import Table from './components/Table/Table'
import Login from './components/login'
import Cadastro from './components/cadastro'
import CadastroSite from './components/cadastroSite'
import CadastroHotel from './components/cadastroHotel'
import {isAuthenticated} from './auth'

const  PrivateRoute = ({component: Component, ...rest}) => (
    <Route 
        {...rest} 
        render={props =>
        isAuthenticated() ? (
            <Component {...props} />
        ) : (
            <Redirect to={{ pathname: '/', state: { from: props.location}}} />
        )
    }/>
);

function Routes(){
    return(
        <BrowserRouter>
            <div className="main_body">
            <Sidebar/>
                <div className='wrapper'>
                    <Topmenu/>
                    <Main/>
                    <Switch>
                        <Route path='/' exact render={Table}/>
                        <Route path='/login' exact render={Login}/>
                        <Route path='/cadastrar/site' exact render={CadastroSite}/>
                        <Route path='/cadastrar/hotel' exact render={CadastroHotel}/>
                        <Route path='/cadastrar' exact render={Cadastro}/>
                        <Route path='/hoteis' exact render={Table}/>
                        <Route path='/sites' exact render={Table}/>
                        <PrivateRoute path='/cadastrar/promocao' exact render={Page}/>
                    </Switch>
                </div>
            </div>
        </BrowserRouter>
    )
}

export default Routes