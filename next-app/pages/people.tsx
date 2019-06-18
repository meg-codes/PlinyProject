import * as React from React
import { withRouter } from 'next/router';
import { element } from 'prop-types';


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

 const CorrespondentList: React.FC<CorrespondentListProps> = ({ correspondents }) => {
  <ul>
    {correspondents.map((el) =>  {
      <li key={el.id}>{el.nomina}</li>
    })}
  </ul>
}