import React from 'react'
import './sidebar.css'
import otelo from '../../static/Otelo.png'



const Sidebar = () => {
    return (
        <div id="mySidebar" class="side_menu">
            <img src="../../static/Otelo.png" style={{paddingLeft:20+'px'}} width="150"/> 
            <ul>
                <br/> 
                <li><a href="javascript:void()" onclick="home()">Início</a></li>
                <li><a href="javascript:void()" onclick="sites()">Sites</a></li>
                <li><a href="javascript:void()" onclick="hoteis()">Hotéis</a></li>
                
                <li><a href="/cadastrar/promocao">Criar Promoção</a></li>
                
            </ul>
        </div>
    )
}

export default Sidebar
