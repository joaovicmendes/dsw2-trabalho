import{getAll} from './getAll'
import {updateTable} from './table.js'

/* eslint-disable */
export function home() {
    // Atualiza a tabela com promoções
    if (isOnHome(window.location.href)) {
        requestAndUpdate('promocao');
        return;
    }
    // Redireciona para a página principal
    window.location.href = "/";
}

export function sites() {
    // Atualiza a tabela com sites
    if (isOnHome(window.location)) {
        requestAndUpdate('site');
        return;
    }

    // Redireciona para a página principal
    window.location.href = "/sites";
}

export function hoteis() {
    // Atualiza a tabela com hotéis
    if (isOnHome(window.location)) {
        requestAndUpdate('hotel');
        return;
    }
    // Redireciona para a página principal
    window.location.href = "/hoteis";
}

export function renderTable(){
    if (window.location == "http://localhost:3000/" 
    || window.location == "http://127.0.0.1:5000/"){
        requestAndUpdate('promocao');
        return;
    }
    if (window.location == "http://localhost:3000/sites" 
    || window.location == "http://127.0.0.1:5000/sites"){
        requestAndUpdate('site');
        return;
    }
    if (window.location == "http://localhost:3000/hoteis" 
    || window.location == "http://127.0.0.1:5000/hoteis"){
        requestAndUpdate('hotel');
        return;
    }
}
function isOnHome(url) {
    return (
        url == "http://localhost:3000/" || url == "http://127.0.0.1:5000/" ||
        url == "http://localhost:3000/sites" || url == "http://127.0.0.1:5000/sites" ||
        url == "http://localhost:3000/hoteis" || url == "http://127.0.0.1:5000/hoteis"      
    );
}

export async function requestAndUpdate(category) {
    const data = await getAll(category);

    if (category === 'promocao') {
        updateTable(category, filterPromocao(Object.values(data.promos)));
    } else if (category === 'hotel') {
        updateTable(category, Object.values(data.hoteis));
    } else if (category === 'site') {
        updateTable(category, Object.values(data.sites));
    }
}

function filterPromocao(promos) {
    const role     = window.localStorage.getItem('role');
    const username = window.localStorage.getItem('username');
    if (role === null || username === null) {
        return promos;
    }

    let filtered = []
    for (let promo of promos) {
        if (role === 'hotel' && promo.cnpj === username)
            filtered.push(promo)
        else if (role === 'site' && promo.site === username)
            filtered.push(promo)
    }
    return filtered;
}

export async function searchPromocao() {
    const queryCity = document.getElementById('queryCity').value.toLowerCase();

    let queryStartDate = new Date(-8640000000000000);
    if (document.getElementById('startDate').value) {
        queryStartDate = new Date(document.getElementById('startDate').value);
    }

    let queryEndDate   = new Date(8640000000000000);
    if (document.getElementById('endDate').value) {
        queryEndDate = new Date(document.getElementById('endDate').value);
    }

    // Requisição para a API
    const data = await getAll('promocao');

    // Filtrando promoções
    const promos = filterPromocao(Object.values(data.promos));
    let filtered = [];

    for (let promo of promos) {
        let promoInicio = new Date(promo.inicio);
        let promoFim = new Date(promo.fim);

        if (promo.cidade.toLowerCase().includes(queryCity) &&
            (promoInicio <= queryEndDate && promoFim >= queryStartDate)) {
            filtered.push(promo);
        }
    }

    updateTable('promocao', filtered);
}

export function deletePromocao(id) {
    const token = window.localStorage.getItem('token');
    let headers = new Headers();
    headers.append('x-access-token', token);
    fetch('http://' + window.location.hostname + ':5000/api/promocao/'+ id, { 
        method: 'DELETE',
        headers: headers
    }).then(
        (response) => {
            if (response.status !== 200) {
                response.json().then(
                    (data) => { 
                        alert(data.message);
                    });
            }
            alert("Promoção deletada com sucesso!");
            home();
        });
}
/* eslint-enable */
