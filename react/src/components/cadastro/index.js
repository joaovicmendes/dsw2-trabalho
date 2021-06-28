import './cadastro.css'

function Cadastro(){
    return(
        <div class="center-div">
            <h2 className="center-text">Que tipo de cadastro gostaria de realizar?</h2>

            <div class="row-div">
                <a class="register_button"  href="/cadastrar/hotel">Novo Hotel</a>
                <a class="register_button"  href="/cadastrar/site">Novo Site</a>
            </div>
        </div>
    )
}

export default Cadastro