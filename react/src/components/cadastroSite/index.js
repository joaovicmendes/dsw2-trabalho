import Helmet from 'react-helmet'
import otelo from '../../static/Otelo.png'

function CadastroSite(){
    return(
        <div class="main">
            <div class="container">
                <form method="post">
                    <h3>Cadastro de Site</h3>
                    <div class="row">
                        <label for="nome" class="col-25">Nome do site</label>
                        <input id="nome"  class="col-75 input_text" name="nome" required />
                    </div>
                    <div class="row">
                        <label for="endereco" class="col-25">Endereço</label>
                        <input id="endereco"  class="col-75 input_text" placeholder="www.nomedosite.com" name="endereco" required />
                    </div>
                    <div class="row">
                        <label for="telefone" class="col-25">Telefone</label>
                        <input id="telefone"  class="col-75 input_text" name="telefone" required />
                    </div>
                    <div class="row">
                        <label for="senha" class="col-25">Senha</label>
                        <input id="senha"  class="col-75 input_text" name="senha" type="password" required />
                    </div>
                    <div class="row">
                        <input type="submit"></input>
                    </div>
                </form>
            </div>
        </div>
    )

}
export default CadastroSite