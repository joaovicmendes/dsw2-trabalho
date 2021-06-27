import React from 'react'
import './Sidebar.css'
import otelo from '../../static/Otelo.png'

function Sidebar() {
    return (
        <div id="mySidebar" class="side_menu">
            <img src={otelo} style={{paddingLeft:20+'px'}} width="150"/> 
            <ul>
                <br/> 
                <li><a href="javascript:void()" onclick="home()">Início</a></li>
                <li><a href="javascript:void()" onclick="sites()">Sites</a></li>
                <li><a href="javascript:void()" onclick="hoteis()">Hotéis</a></li>
                {/* Verificar se está logado */}
                <li><a href="/cadastrar/promocao">Criar Promoção</a></li>
            </ul>
        </div>
    )
}

export default Sidebar
