import React, { useEffect, useState } from "react";
import { home, renderTable } from "../../scripts/home";



function Table(){ 
    renderTable()
    return (
        <div>
            <div id="searchPromocao" class="promocao_filter">
                <div class="filter_field">
                    <label for="queryCity">Cidade:</label>
                    <input id="queryCity" name="queryCity" />
                </div>
                <div class="filter_field">
                    <label for="startDate">Data inicial:</label>
                    <input id="startDate" name="startDate" />
                </div>
                <div class="filter_field">
                    <label for="endDate">Data final:</label>
                    <input id="endDate" name="endDate" />
                </div>
            
                <button type="button" class="btn btn-secondary" onClick="searchPromocao()"
                    id="login-submit-button">Procurar</button>
    
            </div>

            <h2 id="table-title" style={{alignContent:"center"}}>Titulo</h2>
            <div class="table_wrapper">
                <table id="table-content"/>                 
            </div>
        </div>
    )
}

export default Table

