import React  from "react";
import "react-datepicker/dist/react-datepicker.css";
import { searchPromocao, renderTable } from "../../scripts/home";

function Table() {
    renderTable()
    return (
        <div>
            <div id="searchPromocao" className="promocao_filter">
                <div className="filter_field">
                    <label htmlFor="queryCity">Cidade:</label>
                    <input id="queryCity" name="queryCity" />
                </div>
                <div className="filter_field">
                    <label htmlFor="startDate">Data inicial:</label>
                    <input id="startDate" name="startDate" />
                </div>
                <div className="filter_field">
                    <label htmlFor="endDate">Data final:</label>
                    <input id="endDate" name="endDate" />
                </div>
            
                <button type="button" className="btn btn-secondary" onClick={searchPromocao}
                    id="login-submit-button">Procurar</button>
            </div>

            <h2 id="table-title" style={{alignContent:"center"}}>Titulo</h2>
            <div className="table_wrapper">
                <table id="table-content"> 
                </table>
            </div>
        </div>
    )
}

export default Table
