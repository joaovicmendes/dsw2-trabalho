function home() {
    // Atualiza a tabela com promoções
    if (onHome(window.location.href)) {
        getAll('promocao');
        return;
    }
    // Redireciona para a página principal
    window.location.href = "/";
}

function sites() {
    // Atualiza a tabela com sites
    if (onHome(window.location)) {
        getAll('site');
        return;
    }
    // Redireciona para a página principal
    window.location.href = "/sites";
}

function hoteis() {
    // Atualiza a tabela com hotéis
    if (onHome(window.location)) {
        getAll('hotel');
        return;
    }
    // Redireciona para a página principal
    window.location.href = "/hoteis";
}

function getAll(category) {
    // Incluindo token de acesso na requisição
    const token = window.localStorage.getItem('token');
    let headers = new Headers();
    headers.append('x-access-token', token);

    // Requisição para API
    fetch('http://' + window.location.hostname + ':5000/api/' + category, { 
            method: 'GET',
            headers: headers
        })
        .then(
            (response) => {
                if (response.status != 200) {
                    response.json().then(
                        (data) => { 
                            alert(data.message); 
                        });
                    return;
                } 
                
                response.json().then(
                    (data) => {
                        if (category == 'promocao') {
                            updateTable(category, filterPromocao(Object.values(data.promos)));
                        } else if (category == 'hotel') {
                            updateTable(category, Object.values(data.hoteis));
                        } else if (category == 'site') {
                            updateTable(category, Object.values(data.sites));
                        }
                    });
            })
        .catch(
            (err) => {
                console.log('Fetch Error: ', err);
            });
}

function updateTable(category, data) {
    let title = document.getElementById('table-title');
    let table = document.getElementById('table-content');
    let html = '';

    if (category == 'promocao') {
        title.innerText = "Promoções";
        html = promo2table(data);
    } else if (category == 'site') {
        title.innerText = "Sites";
        html = site2table(data);
    } else if (category == 'hotel') {
        title.innerText = "Hotéis";
        html = hotel2table(data);
    }

    table.innerHTML = html;
}

function promo2table(data) {
    let table  = '';
    let header = '';
    let rows   = [];

    // Preenchendo cabeçalho
    let headers = ['Site', 'CNPJ Hotel', 'Nome Hotel', 'Cidade', 'Preço', 'Data início', 'Data fim'];
    if(window.localStorage.getItem('token') != null ){
        headers.push('Options')
    }
    header += '<tr>';
    for (let item of headers) {
        header += '<th>' + item + '</th>';
    }
    header += '</tr>';

    // Preenchendo colunas
    for (let item of data) {
        let row = '';
        row += '<tr>';
        row += "<td>" + item.site   + "</td>";
        row += "<td>" + item.cnpj   + "</td>";
        row += "<td>" + item.hotel   + "</td>";
        row += "<td>" + item.cidade   + "</td>";
        row += "<td>" + item.preco  + "</td>";
        row += "<td>" + item.inicio + "</td>";
        row += "<td>" + item.fim    + "</td>";
        if(window.localStorage.getItem('token') != null ){
            row += "<td>" + '<button onclick="deletePromocao('+item.id+')">Delete</button>' + "</td>";
        }
        row += '</tr>';
        rows.push(row);
    }

    // Montando tabela
    table += header;
    for (let row of rows)
        table += row;

    return table;
}

function site2table(data) {
    let table  = '';
    let header = '';
    let rows   = [];

    // Preenchendo cabeçalho
    const headers = ['Nome', 'Endereço (URL)', 'Telefone'];
    header += '<tr>';
    for (let item of headers) {
        header += '<th>' + item + '</th>';
    }
    header += '</tr>';

    // Preenchendo colunas
    for (let item of data) {
        let row = '';
        row += '<tr>';
        row += "<td>" + item.nome   + "</td>";
        row += "<td>" + item.endereco   + "</td>";
        row += "<td>" + item.telefone  + "</td>";
        row += '</tr>';
        rows.push(row);
    }

    // Montando tabela
    table += header;
    for (let row of rows)
        table += row;

    return table;
}

function hotel2table(data) {
    let table  = '';
    let header = '';
    let rows   = [];

    // Preenchendo cabeçalho
    const headers = ['Nome', 'CNPJ', 'Cidade'];
    header += '<tr>';
    for (let item of headers) {
        header += '<th>' + item + '</th>';
    }
    header += '</tr>';

    // Preenchendo colunas
    for (let item of data) {
        let row = '';
        row += '<tr>';
        row += "<td>" + item.nome    + "</td>";
        row += "<td>" + item.cnpj    + "</td>";
        row += "<td>" + item.cidade  + "</td>";
        row += '</tr>';
        rows.push(row);
    }

    // Montando tabela
    table += header;
    for (let row of rows)
        table += row;

    return table;
}

function filterPromocao(promos) {
    const role     = window.localStorage.getItem('role');
    const username = window.localStorage.getItem('username');
    if (role == null || username == null) {
        return promos;
    }

    let filtered = []
    for (let promo of promos) {
        if (role == 'hotel' && promo.cnpj == username)
            filtered.push(promo)
        else if (role == 'site' && promo.site == username)
            filtered.push(promo)
    }
    return filtered;
}

function onHome(url) {
    return (
        url == "http://localhost:5000/" || url == "http://127.0.0.1:5000/" ||
        url == "http://localhost:5000/sites" || url == "http://127.0.0.1:5000/sites" ||
        url == "http://localhost:5000/hoteis" || url == "http://127.0.0.1:5000/hoteis"      
    );
}

function searchPromocao() {
    const queryCity = document.getElementById('queryCity').value.toLowerCase();
    let queryStartDate = new Date(-8640000000000000);
    let queryEndDate   = new Date(8640000000000000);

    if (document.getElementById('startDate').value) {
        queryStartDate = new Date(document.getElementById('startDate').value);
    }

    if (document.getElementById('endDate').value) {
        queryEndDate = new Date(document.getElementById('endDate').value);
    }

    // @TODO: da pra colocar essa requisição em uma nova função, mas tem que usar async/await
    // Incluindo token de acesso na requisição
    const token = window.localStorage.getItem('token');
    let headers = new Headers();
    headers.append('x-access-token', token);

    // Requisição para API
    fetch('http://' + window.location.hostname + ':5000/api/promocao', { 
            method: 'GET',
            headers: headers
        })
        .then(
            (response) => {
                if (response.status != 200) {
                    response.json().then(
                        (data) => { 
                            alert(data.message); 
                        });
                    return;
                } 
                
                response.json().then(
                    (data) => {
                        let promos = filterPromocao(Object.values(data.promos));
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
                    });
            });
}

function deletePromocao(id) {
    const token = window.localStorage.getItem('token');
    let headers = new Headers();
    headers.append('x-access-token', token);
    fetch('http://' + window.location.hostname + ':5000/api/promocao/'+ id, { 
        method: 'DELETE',
        headers: headers
    }).then(
        (response) => {
            if (response.status != 200) {
                response.json().then(
                    (data) => { 
                        alert(data.message);
                    });
            }
            alert("Promoção deletada com sucesso!");
            home();
        });
}
