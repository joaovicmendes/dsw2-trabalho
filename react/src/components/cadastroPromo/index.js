import Helmet from 'react-helmet'
import otelo from '../../static/Otelo.png'

function CadastroPromo(){
    return(
        <form method="post" class="main">
            <div class="container">
                <div class="row">
                    {% if data.role == 'hotel' %}
                    <label for="nome_site"  class="col-25" >Site</label>
                        <div class="col-75">
                            <select id="nome_site" name="nome_site" required >
                                {% for site in sites %}
                                    <option value="{{site.nome}}">{{ site.nome }}</option>
                                {% endfor %}
                            </select>
                        </div>
                    {% endif %}
                    {% if data.role == 'site' %}
                        <label for="nome_hotel"  class="col-25" >Hotel</label>
                            <div class="col-75">
                                <select id="nome_hotel" name="nome_hotel" required >
                                    {% for hotel in hoteis %}
                                        <option value="{{hotel.nome}}">{{ hotel.nome }}</option>
                                    {% endfor %}
                                </select>
                            </div>
                    {% endif %}
                </div>

                <div class="row">
                    <label for="preco" class="col-25">Preço (R$)</label>
                    <input id="preco" type="number" class="col-75 input_text" name="preco" required />
                </div>
                <div class="row">
                    <label for="data-ini" class="col-25">Data início (opcional):</label>
                    <input id="data-ini" class="col-75 input_text" name="data-ini" />
                </div>
                <div class="row">
                    <label for="data-fim" class="col-25">Data fim (opcional):</label>
                    <input id="data-fim" class="col-75 input_text" name="data-fim" />
                </div>
                <div class="row">
                    <button class="register_button" type="button" onClick="createPromo()">Cadastrar</button>
                </div>
            </div>
        </form>
   )

}

export default  CadastroPromo