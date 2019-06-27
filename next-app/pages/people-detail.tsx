import * as React from 'react';
import Head from 'next/head';
import { withRouter,  WithRouterProps } from 'next/router';
import axios from 'axios'

import Header from '../components/Header'

interface DetailedPerson {
    id: number
    letters_to: Array<String>,
    citations: Array<String>,
    nomina: string
    gender: string,
    citizen: string,
    equestrian: string,
    senatorial: string,
    consular: string,
    birth: number,
    death: number,
    cos: number,
    cos_suff: number,
    floruit: number,
    certainty_of_id: number,
    notes: string,
    from_comum: boolean,
    mentioned_in: Array<String>
    related_to: Array<String>

}

interface PersonDetailProps extends WithRouterProps {
    id: number,
    person?: DetailedPerson
}

function slugify(str: string): string {
    return str.toLowerCase().replace(/\./g, '').split(' ').join('-');
}

function hasDates(person: DetailedPerson): boolean {
    return Boolean(person.birth || person.death || person.cos || person.cos_suff
        || person.floruit)
}

const PersonDates: React.FC<{hasDates: boolean}> = ({ hasDates }) => {
    if (hasDates) {
        return (<section>
            I have dates!
        </section>)
    }
    return ('')
}

class PersonDetail extends React.Component<PersonDetailProps> {

    constructor(props: PersonDetailProps) {
        super(props)
    }

    componentDidMount() {
        // map references for a tidier set of calls below
        const router = this.props.router
        const person = this.props.person
        const id = this.props.id

        if (router && person &&
            router.asPath.search(slugify(person.nomina)) === -1) {
                router.push(`/person-detail?id=${id}`,
                    `/people/${slugify(person.nomina)}-${id}`)
        }

    }

    render() {
        const person = this.props.person
        if (!person) {
            return (
                <React.Fragment>

                    <Head><title>No person data loaded.</title></Head>
                    <Header />
                        <main>
                            <h1>No person data loaded.</h1>
                            <p>This may indicate an error in the data API that supports
                                PlinyProject.org.
                            </p>
                        </main>
                </React.Fragment>
            )
        }

        return (
            <React.Fragment>

                <Head>
                    <title>{person.nomina}</title>
                </Head>
                <main>
                    <Header />
                    <h1>{person.nomina}</h1>
                    <div className='person-details'>
                        <section>
                            <div>
                                <h2>Social Class Info</h2>
                            </div>
                            <ul>
                                <li>Citizen: {person.citizen}</li>
                                <li>Equestrian: {person.equestrian}</li>
                                <li>Senatorial: {person.senatorial}</li>
                                <li>Consular: {person.consular}</li>
                            </ul>
                        </section>
                        <PersonDates hasDates={hasDates(person)} />
                    </div>
                </main>


            </React.Fragment>
        )
    }

    static async getInitialProps({ req, query}: any) {
        const id = query.id || 1
        try {
            const baseUrl = req ? `${req.protocol}://${req.get('Host')}` : '';
            const res = await axios.get(baseUrl + `/api/people/${id}`);
            return {
                id: id,
                person: res.data
            }
        }
        catch(err) {

            return {
                id: id,
                person: null
            }
        }
    }
}

export default withRouter(PersonDetail)