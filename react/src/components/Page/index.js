import Helmet from 'react-helmet'
import Table from '../table'
import otelo from '../../static/Otelo.svg'

function Page() {
    return (
        <div>
            <Helmet>
                <meta charset="UTF-8"/>
                <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
                <title>Otelo</title>
                <link rel="icon" href={ otelo }/>
            </Helmet>

            <div class="main_body">
                <div class='wrapper'>
                    <Table/>
                </div>
            </div>
        </div>
    )
}

export default Page
