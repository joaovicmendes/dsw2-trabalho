import React from 'react';
import getToken from '../../scripts/login'

const Login = () => {
    return (
        <div class="container"> 
            <form method="post" id="login-form">
                <h3>Login</h3>
                <div class="row"> 
                    <label for="username" class="col-25">Nome de usuário</label>
                    <input id= "username" class="col-75 input_text" placeholder="CNPJ ou URL" name="username" required /> <br/>
                </div>    

                <div class="row"> 
                    <label for="password" class="col-25">Senha</label>
                    <input id= "password" class="col-75 input_text" name="password" type="password" required/> <br/>
                </div>

                <div class="row"> 
                    <input type="submit" onClick={getToken} id="login-submit-button"></input>
                </div>
            </form>
        </div>
    )
}

export default Login