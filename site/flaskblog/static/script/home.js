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
                            updateTable(category, data.promos);
                        } else if (category == 'hotel') {
                            updateTable(category, data.hoteis);
                        } else if (category == 'site') {
                            updateTable(category, data.sites);
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
    const headers = ['Site', 'CNPJ Hotel', 'Preço', 'Data início', 'Data fim'];
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
        row += "<td>" + item.preco  + "</td>";
        row += "<td>" + item.inicio + "</td>";
        row += "<td>" + item.fim    + "</td>";
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
