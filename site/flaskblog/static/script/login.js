function get_token() {
    let headers = new Headers();
    const username = document.querySelector('#username').value;
    const password = document.querySelector('#password').value;
    headers.append('Authorization', 'Basic ' + btoa(username + ":" + password));

    fetch('http://'+window.location.hostname+':5000/api/token', { method: 'POST', headers: headers})
    .then(function(response) {
        console.log(response);
        if (response.status != 200) {
            response.json().then( data => {alert(data.message);} );
        } else {
            response.json().then(data => {
                window.localStorage.setItem('token', data.token); })
                document.getElementById('login-form').submit()
        }
    })
    .catch(function(err) {
      console.log('Fetch Error: ', err);
    });
};
