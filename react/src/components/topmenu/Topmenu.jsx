import React from 'react'
import './Topmenu.css'

function Topmenu() {
    return (
        <div class="top_menu">
                <ul>
                    {/* Checar se esta logado */}
                    {/* <li><a href="/logout">Logout</a></li> */}
                    {/* <li> Nome do usuário logado</li> */}
                    
                    <li><a href="/login">Login</a></li>
                    <li><a href="/cadastrar">Cadastrar</a></li>  
                </ul>
            </div>
    )
}

export default Topmenu
