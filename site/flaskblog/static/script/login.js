function send_login_info() {
    let headers = new Headers();
    const username = document.querySelector('#username').value;
    const password = document.querySelector('#password').value;
    headers.append('Authorization', 'Basic ' + btoa(username + ":" + password));

    fetch(window.location.href, { method: 'POST', headers: headers})
    .then(function(response) {
        console.log(response);
        if (response.status != 200) {
            response.json().then(data => {alert(data.message);});
            window.location.reload();
        } else {
            response.json().then(data => {
                window.localStorage.setItem('token', data.token);
                window.location.href = "http://127.0.0.1:5000/"});
                // @TODO: precisa ver como fazer js fazer o request sem dar trigger no botão, com a solução atual
                // clicando no botão funciona certo, mas a tecla enter não faz nada.
        }
    })
    .catch(function(err) {
      console.log('Fetch Error: ', err);
    });
};
