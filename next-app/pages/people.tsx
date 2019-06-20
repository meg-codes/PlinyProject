import * as React from 'react';
import axios from 'axios';
import { NextFunctionComponent, QueryStringMapObject } from 'next';
import Link from 'next/link';

import Header from '../components/Header';
import PeopleFilter from '../components/PeopleFilter';

interface Person {
  pk: number
  nomina: string,
  ordo: string,
  letters_to: Array<string>,
  url: URL
}

interface CorrespondentListProps {
  correspondents: Array<Person>,
}

interface PaginationProps {
  query: QueryStringMapObject,
  count: number
  page: number
}

interface PeopleListProps extends CorrespondentListProps, PaginationProps {}

interface PaginationState {
  pages: Array<number>
}

function queryMapToString(query: QueryStringMapObject) {

    const queryArray = [];
    if (query) {
      for (let prop in query) {
        if (Array.isArray(query[prop])) {
          //@ts-ignore
          query[prop].forEach((el) => {
            queryArray.push(`${prop}=${el}`)
          })
        } else {
          queryArray.push(`${prop}=${query[prop]}`);
        }
      }

      if (queryArray.length > 0) {
        return `?${queryArray.join('&')}`
      }
    }

    return ''
}

class Pagination extends React.Component<PaginationProps, PaginationState> {
  constructor(props: PaginationProps) {
    super(props)

    this.state = {
      pages: [...Array(Math.ceil(this.props.count / 20)).keys()].map(x => x+1)
    }
  }

  render() {
    return (
      <nav aria-label='pagination navigation'>
        <ul className='pagination'>
          {this.state.pages.map((el) => {
            if (el == this.props.page) {
              return (<li>
                        <a href="#" className='disabled'
                        aria-label={`${el} is current page`}
                        tabIndex={-1}>{el}</a>
                      </li>)
            }
            this.props.query.page = el.toString()
            const queryString = queryMapToString(this.props.query)
            return (<li key={el}>
                      <Link href={`/people${queryString}`}>
                          <a aria-label={`Link to page ${el}`}>{el}</a>
                      </Link>
                    </li>)
          })}
        </ul>
      </nav>
    )
  }
}


 const CorrespondentList: React.FC<CorrespondentListProps> = ({ correspondents }) => (
   <div className="responsive-table">
    <table>
      <thead>
        <tr>
          <th>Nomina</th>
          <th>Ordo (Social Class)</th>
          <th>Letters To</th>
        </tr>
      </thead>
      <tbody>
      {correspondents.map((el) => (
        <tr key={el.pk}>
          <td><Link href={el.url}><a>{el.nomina}</a></Link></td>
          <td>{el.ordo}</td>
          <td>{el.letters_to.join(', ')}</td>
        </tr>
      ))}
      </tbody>
    </table>
  <style jsx>
    {`div {
      overflow-x: auto;
    }`}
  </style>
  </div>

 )

const PeopleList: NextFunctionComponent<PeopleListProps> = ({correspondents, count, page, query}) => (
  <React.Fragment>
  <Header />
  <main>
    <h1>Pliny's Correspondents</h1>
    <p>
      Below is a list of Pliny's correspondents. You may use the form below to
      filter the results by name or nomina.
    </p>
    <PeopleFilter query={query} />
    <Pagination count={count} page={page} query={query} />
    <CorrespondentList correspondents={correspondents}/>
  </main>
  </React.Fragment>
)

PeopleList.getInitialProps = async ({ query, req }: any) => {
  try {

    const queryString = queryMapToString(query)
    const baseUrl = req ? `${req.protocol}://${req.get('Host')}` : '';
    const res = await axios.get(baseUrl + `/api/people${queryString}`);
    return {
        correspondents: res.data.results,
        count: res.data.count,
        page: query.page ? query.page : 1,
        query: query
    }
  } catch(err) {
    return {
      correspondents: [],
      count: 0,
      page: query.page ? query.page : 1,
      query: query
    }
  }
}

export default PeopleList;