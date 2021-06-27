import React from 'react'
import './main.css'
import {home} from '../../scripts/home'
import '../table/table'
import Table from '../table/table'

const Main = () => {
    
    
    //var data_arr = Object.values(data);
    //console.log(data)
    return (
        <div class="main" id="main">
            
                <button id ="openbtn"  class="openbtn" onclick="openNav()">☰</button>
                <button id ="closebtn" class="closebtn" onclick="closeNav()">☰</button>
                <Table/>
        </div>
    )
}

export default Main
