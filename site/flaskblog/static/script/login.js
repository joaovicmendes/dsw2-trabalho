function getToken() {
    // Montando cabeçalho e extraindo campos username e password do formulário
    const username = document.querySelector('#username').value;
    const password = document.querySelector('#password').value;
    let headers = new Headers();
    headers.append('Authorization', 'Basic ' + btoa(username + ":" + password));

    // Requisição para a API
    fetch('http://' + window.location.hostname + ':5000/api/token', { 
            method: 'POST', 
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
                    // Como a requisição foi bem sucedida, guarda o token localmente
                    // para requisições futuras. Depois envia o formulário para fazer
                    // autenticação de sessão
                    response.json().then(
                        (data) => {
                            window.localStorage.setItem('token', data.token); 
                        })
                    document.getElementById('login-form').submit()
                }
            })
        .catch( 
            (err) => {
                console.log('Fetch Error: ', err); 
            });
};
