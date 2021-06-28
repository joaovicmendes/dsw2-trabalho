import React from 'react'
import './sidebar.css'
import otelo from '../../static/Otelo.png'
import { home, sites, hoteis } from '../../scripts/home'

function Sidebar() {
    return (
        <div id="mySidebar" className="side_menu">
            <img src={otelo} style={{paddingLeft:20+'px'}} width="150" alt="Otelo"/> 
            <ul>
                <br/>
                <li><a onClick={ home }>Início</a></li>
                <li><a onClick={ sites }>Sites</a></li>
                <li><a onClick={ hoteis }>Hotéis</a></li>
                {/* Verificar se está logado */}
                <li><a href="/cadastrar/promocao">Criar Promoção</a></li>
            </ul>
        </div>
    )
}

export default Sidebar
