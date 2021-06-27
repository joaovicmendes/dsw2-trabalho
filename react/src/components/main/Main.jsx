import React from 'react'
import './Main.css'

function Main() {
    return (
        <div class="main" id="main">
            <button id ="openbtn"  class="openbtn" onclick="openNav()">☰</button>
            <button id ="closebtn" class="closebtn" onclick="closeNav()">☰</button>     
        </div>
    )
}

export default Main
