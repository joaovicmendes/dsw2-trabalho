import './style.css'

function CadastroHotel(){
    return(
        <form method="post" class="main">
            <div className="container">
                <h3>Cadastro de Hotel</h3>
                <div class="row">
                    <label for="nome" class="col-25">Nome</label>
                    <input id="nome" class="col-75 input_text" name="nome" required />
                </div>
                <div class="row">
                    <label for="cnpj" class="col-25">CNPJ</label>
                    <input id="cnpj"  class="col-75 input_text" name="cnpj" required />
                </div>
                <div class="row">
                    <label for="cidade" class="col-25">Cidade</label>
                    <input id="cidade"  class="col-75 input_text" name="cidade" required />
                </div>
                <div class="row">
                    <label for="senha" class="col-25">Senha</label>
                    <input id="senha"  class="col-75 input_text" name="senha" type="password" required />
                </div>
                <div class="row">
                    <input type="submit"></input>
                </div>
            </div>
        </form>
    )

}
export default CadastroHotel