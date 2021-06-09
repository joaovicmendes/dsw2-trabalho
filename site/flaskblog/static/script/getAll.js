async function getAll(category) {
    // Incluindo token de acesso na requisição
    const token = window.localStorage.getItem('token');
    let headers = new Headers();
    headers.append('x-access-token', token);

    // Requisição para API
    const response = await fetch('http://' + window.location.hostname + ':5000/api/' + category, { 
            method: 'GET',
            headers: headers
        })
        
    if (response.status != 200) {
        response.json().then(
            (data) => { 
                alert(data.message); 
            });
        return;
    } 

    return await response.json();
}
