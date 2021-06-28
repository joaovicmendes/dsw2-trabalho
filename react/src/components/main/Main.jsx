import React from 'react'
import {openNav, closeNav} from '../../scripts/menu'
import './Main.css'

function Main() {
    return (
        <div className="main" id="main">
                <button id ="openbtn"  className="openbtn" onClick={ openNav }>☰</button>
                <button id ="closebtn" className="closebtn" onClick={ closeNav }>☰</button>
        </div>
    )
}

export default Main
