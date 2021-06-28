import React  from "react";
import './table.css'
import { searchPromocao, renderTable } from "../../scripts/home";

function Table() {
    renderTable()
    return (
        <div>
            <h2 id="table-title" className="table-title" style={{alignContent:"center"}}>Titulo</h2>
            <div className="center">
                <div id="searchPromocao" className="promocao_filter">
                    <div className="filter_field">
                        <label htmlFor="queryCity">Cidade</label>
                        <input className="field" id="queryCity"type="text" name="queryCity" />
                    </div>
                    <div className="filter_field">
                        <label htmlFor="startDate">Data inicial</label>
                        <input className="field"id="startDate"type="text" name="startDate" />
                    </div>
                    <div className="filter_field">
                        <label htmlFor="endDate">Data final  </label>
                        <input className="field" id="endDate" type="text" name="endDate" />
                    </div>
                    <div className="filter_field">
                    <button type="button" className="promo-button" onClick={searchPromocao}
                        id="login-submit-button">Procurar</button>
                    </div>
                </div>
            </div>
                <div className="table_wrapper">
                    <table id="table-content"> 
                    </table>
                </div>
        </div>
    )
}

export default Table
