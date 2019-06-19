import * as React from 'react';
import axios from 'axios';
import { NextFunctionComponent } from 'next';

import Header from '../components/Header';

interface Person {
  pk: number
  nomina: string,
  ordo: string,
  lettersTo: Array<string>,
  url: URL
}

interface CorrespondentListProps {
  correspondents: Array<Person>
}

 const CorrespondentList: React.FC<CorrespondentListProps> = ({ correspondents }) => (
   <ul>
    {correspondents.map((el) =>
      <li key={el.pk}>{el.nomina}</li>
    )}
  </ul>
 )

const PeopleList: NextFunctionComponent<CorrespondentListProps> = ({correspondents}) => (
  <div>
  <Header />
  <main>
    <CorrespondentList correspondents={correspondents} />
  </main>
  </div>
)

PeopleList.getInitialProps = async ({ req }: any) => {
  try {
    const i = req.originalUrl.indexOf('?');
    const query = i+1 ? req.originalUrl.substr(i) : ''
    const baseUrl = req ? `${req.protocol}://${req.get('Host')}` : '';
    const res = await axios.get(baseUrl + `/api/people${query}`);
    return {
        correspondents: res.data.results
    }
  } catch(err) {
    return {
      correspondents: []
    }
  }
}

export default PeopleList;