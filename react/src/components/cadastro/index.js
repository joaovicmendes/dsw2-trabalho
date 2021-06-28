import Helmet from 'react-helmet'
import otelo from '../../static/Otelo.png'
function Cadastro(){
    return(
        <div class="main">
    <h3>Que tipo de cadastro gostaria de realizar?</h3>
    <div class="row" style={{marginLeft:"20%"}}>
        <a class="register_button" style={{float: "left", marginRight:"10px"}} href="/cadastrar/hotel">Novo Hotel</a>
        <a class="register_button" style={{float: "left"}} href="/cadastrar/site">Novo Site</a>
    </div>
</div>
    )
}

export default Cadastro