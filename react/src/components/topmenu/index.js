import React from 'react'
import './topmenu.css'
import otelo from '../../static/Otelo.png'

import { home, sites, hoteis } from '../../scripts/home'


function Topmenu() {
    return (
        <div className="top_menu">
                <ul>
                    {/* Checar se esta logado */} 
                    {/* <li><a href="/logout">Logout</a></li> */}
                    {/* <li> Nome do usuário logado</li> */}
                    
                    <li><a className="top-button" href="/cadastrar">Cadastrar</a></li>  
                    <li><a className="top-button" href="/login">Login</a></li>
                    <div className="top-left-align">
                        <li><button className="top-button" onClick={ hoteis }>Hotéis</button></li>
                        <li><button className="top-button" onClick={ sites }>Sites</button></li>
                        <li><button className="top-button" onClick={ home }>Promoções</button></li>
                        
                        <li className="top-button bold logo" >Otelo</li> 
                        <li><img className="top-button logo" src={otelo} width="150" alt="Otelo"/> </li>
                        
                    </div>
                    
                </ul>
            </div>

    )
}

export default Topmenu

/*
        <div className="top_menu">
                <ul>
                    {/* Checar se esta logado } */
                    {/* <li><a href="/logout">Logout</a></li> */}
                    {/* <li> Nome do usuário logado</li> */}
                    /*
                    <li><a href="/login">Login</a></li>
                    <li><a href="/cadastrar">Cadastrar</a></li>  
                    <li><button onClick={ home }>Início</button></li>
                    <li><button onClick={ sites }>Sites</button></li>
                    <li><button onClick={ hoteis }>Hotéis</button></li>
                    
                </ul>
            </div>
            */