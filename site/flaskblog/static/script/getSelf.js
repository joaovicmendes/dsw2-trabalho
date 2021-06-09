async function getSelf() {
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
    let response = await fetch('http://' + window.location.hostname + ':5000/api/user', { 
            method: 'GET',
            headers: headers
        });

    if (response.status != 200) {
        const data = await response.json();
        alert(data.message);
        return null;
    }

    const data = await response.json();
    return data;
}
