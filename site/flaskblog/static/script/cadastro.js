function create_promo() {
    get_self();
}

function new_promo(user) {
    // Incluindo token de acesso na requisição
    let headers = new Headers();
    const token = window.localStorage.getItem('token');
    headers.append('x-access-token', token);

    let promo = {nome_site: '', nome_hotel: '', preco: '', ini: '', fim: ''};
    console.log(user)
    if (user.role == "site") {
        promo.nome_site = user.nome;
        promo.nome_hotel = document.getElementById('nome_hotel').value;
    }
    else if (user.role == "hotel") {
        promo.nome_hotel = user.nome;
        promo.nome_site  = document.getElementById('nome_site').value;
    }
    promo.preco = document.getElementById('preco').value;
    promo.ini   = document.getElementById('data-ini').value;
    promo.fim   = document.getElementById('data-fim').value;
    console.log(promo)

    // Requisição para API
    fetch(('http://'+ window.location.hostname + ':5000/api/promocao'), { method: 'POST', headers: headers, body: JSON.stringify(promo)})
    .then(function(response) {
        console.log("Requisição de criação de promoção enviada.");
        if (response.status != 201) {
            response.json().then( data => { alert(data.message); });
        } else {
            response.json().then( data => {
                alert(data.message + "\nClique em OK para ir para a página principal.");
                window.location.href = "/";
            });
        }
    })
    .catch(function(err) {
      console.log('Fetch Error: ', err);
    });
};

function get_self() {
    // Incluindo token de acesso na requisição
    let headers = new Headers();
    const token = window.localStorage.getItem('token');
    headers.append('x-access-token', token);

    // Requisição para API
    console.log("Requisição para pegar usuário");
    fetch(('http://'+ window.location.hostname + ':5000/api/user'), { method: 'GET', headers: headers})
    .then(function(response) {
        if (response.status != 200) {
            response.json().then( data => { alert(data.message); });
        } else {
            response.json().then( data => {
                console.log(data);
                new_promo(data);
            });
        }
    });
}
