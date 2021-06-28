export function updateTable(category, data) {
    let title = document.getElementById('table-title');
    let table = document.getElementById('table-content');
    let html = '';
    let divSearchPromocao = document.getElementById("searchPromocao");

    if (category === 'promocao') {
        title.innerText = "Promoções";
        html = promo2table(data);
        divSearchPromocao.style.display = '';
    } else if (category === 'site') {
        title.innerText = "Sites";
        html = site2table(data);
        divSearchPromocao.style.display = 'none';
    } else if (category === 'hotel') {
        title.innerText = "Hotéis";
        html = hotel2table(data);
        divSearchPromocao.style.display = 'none';
    }

    // Se número de Promoções/Sites/Hotéis for zero, avisa que não foram encontrados resultados
    if (Object.keys(data).length === 0) {
        title.innerText += " - Nenhum resultado encontrado";
    }

    table.innerHTML = html;
}

function promo2table(data) {
    let table  = '';
    let header = '';
    let rows   = [];

    // Preenchendo cabeçalho
    let headers = ['Site', 'CNPJ Hotel', 'Nome Hotel', 'Cidade', 'Preço', 'Data início', 'Data fim'];
    if(window.localStorage.getItem('token') !== null ){
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
        if(window.localStorage.getItem('token') !== null ){
            row += '<td><button onclick="deletePromocao(' + item.id + ')">Delete</button></td>';
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
