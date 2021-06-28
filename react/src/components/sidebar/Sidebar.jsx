import React from 'react'
import './Sidebar.css'
import otelo from '../../static/Otelo.png'
import { home, sites, hoteis } from '../../scripts/home'

function Sidebar() {
    return (
        <div id="mySidebar" className="side_menu">
            <img src={otelo} style={{paddingLeft:20+'px'}} width="150" alt="Otelo"/> 
            <ul>
                <br/>
                <li><button onClick={ home }>Início</button></li>
                <li><button onClick={ sites }>Sites</button></li>
                <li><button onClick={ hoteis }>Hotéis</button></li>
                {/* Verificar se está logado */}
                <li><a href="/cadastrar/promocao">Criar Promoção</a></li>
            </ul>
        </div>
    )
}

export default Sidebar
