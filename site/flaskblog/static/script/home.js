function get_all_promos() {
    let headers = new Headers();
    const token = window.localStorage.getItem('token');
    headers.append('x-access-token', token);

    fetch(('http://'+ window.location.hostname + ':5000/api/promocao'), { method: 'GET', headers: headers})
    .then(function(response) {
        console.log(response);
        if (response.status != 200) {
            response.json().then( data => { alert(data.message); });
        } else {
            response.json().then( data => { update_table('promocao', data.promos); } );
        }
    })
    .catch(function(err) {
      console.log('Fetch Error: ', err);
    });
};

function get_role_promos(role) {
    let headers = new Headers();
    const token = window.localStorage.getItem('token');
    headers.append('x-access-token', token);

    fetch('http://'+window.location.hostname+':5000/api/promocao/'+role, { method: 'GET', headers: headers})
    .then(function(response) {
        console.log(response);
        if (response.status != 200) {
            response.json().then( data => { alert(data.message); });
        } else {
            response.json().then( data => { update_table(data.promos); } );
        }
    })
    .catch(function(err) {
      console.log('Fetch Error: ', err);
    });
};

function get_hotel_promos() { get_role_promos('hotel'); }
function get_site_promos()  { get_role_promos('site');  }

function update_table(type, data) {
    let table = document.getElementById('main-table-content');
    let html = "";
    if (type == 'promocao') {
        for (item of data) {
            html += '<tr>';
            html += "<td>" + item.site   + "</td>";
            html += "<td>" + item.cnpj   + "</td>";
            html += "<td>" + item.preco  + "</td>";
            html += "<td>" + item.inicio + "</td>";
            html += "<td>" + item.fim    + "</td>";
            html += '</tr>';
        }
    }
    else if (type == 'site') {

    }
    else if (type == 'hotel') {

    }

    table.innerHTML = html;
}

get_all_promos();
