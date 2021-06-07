function createPromo() {
    getSelf();
}

function newPromo(user) {
    // Incluindo token de acesso na requisição
    const token = window.localStorage.getItem('token');
    let headers = new Headers();
    headers.append('x-access-token', token);

    // Criando objeto da promoção
    let promo = {
        nome_site: '',
        nome_hotel: '', 
        preco: '',
        ini: '',
        fim: ''
    };
    if (user.role == "site") {
        promo.nome_site = user.nome;
        promo.nome_hotel = document.getElementById('nome_hotel').value;
    } else if (user.role == "hotel") {
        promo.nome_hotel = user.nome;
        promo.nome_site  = document.getElementById('nome_site').value;
    }
    promo.preco = document.getElementById('preco').value;
    promo.ini   = document.getElementById('data-ini').value;
    promo.fim   = document.getElementById('data-fim').value;

    // @TODO: validar dados do formulário com JS

    // Requisição para API
    fetch('http://' + window.location.hostname + ':5000/api/promocao', {
            method: 'POST',
            headers: headers,
            body: JSON.stringify(promo)
        })
    .then(
        (response) => {
            console.log("Requisição de criação de promoção enviada.");
            if (response.status != 201) {
                response.json().then( 
                    (data) => {
                        alert(data.message); 
                    });
            } else {
                response.json().then(
                    (data) => {
                        alert(data.message + "\nClique em OK para ir para a página principal.");
                        window.location.href = "/";
                    });
            }
        })
    .catch(
        (err) => {
        console.log('Fetch Error: ', err);
        });
}

function getSelf() {
    // Incluindo token de acesso na requisição
    const token = window.localStorage.getItem('token');
    if (token == null) {
        alert("Token inexistente/expirado. Faça login novamente.");
        window.location.href = "/logout";
        return;
    }

    let headers = new Headers();
    headers.append('x-access-token', token);

    // Requisição para API
    fetch('http://' + window.location.hostname + ':5000/api/user', { 
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
                } else {
                    response.json().then(
                        (data) => {
                            newPromo(data);
                        });
                }
            })
        .catch( 
            (err) => {
                console.log('Fetch Error: ', err); 
            });
}
