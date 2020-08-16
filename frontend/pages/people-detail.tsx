import * as React from "react";
import Head from "next/head";
import axios from "axios";

import Header from "../components/Header";
import { NextPageContext } from "next";
import getBaseUrl from "./util";

export interface DetailedPerson {
  id: number;
  letters_to: Array<string>;
  citations: Array<string>;
  nomina: string;
  gender: string;
  citizen: string;
  equestrian: string;
  senatorial: string;
  consular: string;
  birth: number | null;
  death: number | null;
  cos: number | null;
  cos_suff: number | null;
  floruit: number | null;
  certainty_of_id: number | null;
  notes: string;
  from_comum: boolean;
  mentioned_in: Array<string>;
  related_to: Array<string>;
}

interface PersonDetailProps {
  id: number;
  person?: DetailedPerson;
}

function slugify(str: string): string {
  return str.toLowerCase().replace(/\./g, "").split(" ").join("-");
}

function hasDates(person: DetailedPerson): boolean {
  return Boolean(
    person.birth ||
      person.death ||
      person.cos ||
      person.cos_suff ||
      person.floruit
  );
}

interface Dates {
  birth: number | null;
  death: number | null;
  cos: number | null;
  cos_suff: number | null;
  floruit: number | null;
  [index: string]: number | null;
}

interface PersonDateProps {
  hasDates: boolean;
  dates: Dates;
}

const PersonDates: React.FC<PersonDateProps> = ({ hasDates, dates }) => {
  if (hasDates) {
    return (
      <section>
        <div>
          <h2>Key Dates</h2>
        </div>
        <ul>
          {Object.keys(dates).map((key) => {
            switch (key) {
              case "cos": {
                if (dates.cos) {
                  return <li key={key}>Cos. {dates.cos}</li>;
                }
                break;
              }
              case "cos_suff": {
                if (dates.cos_suff) {
                  return <li key={key}>Cos. suff.: {dates.cos_suff}</li>;
                }
                break;
              }

              case "birth": {
                if (dates.birth) {
                  return <li key={key}>Birth: {dates.birth}</li>;
                }
                break;
              }

              case "death": {
                if (dates.death) {
                  return <li key={key}>Death: {dates.death}</li>;
                }
                break;
              }

              case "floruit": {
                if (dates.floruit) {
                  return <li key={key}>Floruit: {dates.floruit}</li>;
                }
                break;
              }
            }
          })}
        </ul>
      </section>
    );
  }
  return <section></section>;
};

class PersonDetail extends React.Component<PersonDetailProps> {
  constructor(props: PersonDetailProps) {
    super(props);
  }

  render() {
    const person = this.props.person;
    if (!person) {
      return (
        <React.Fragment>
          <Head>
            <title>No person data loaded.</title>
          </Head>
          <Header />
          <main>
            <h1>No person data loaded.</h1>
            <p>
              This may indicate an error in the data API that supports
              PlinyProject.org.
            </p>
          </main>
        </React.Fragment>
      );
    }

    return (
      <React.Fragment>
        <Head>
          <title>{person.nomina}</title>
        </Head>
        <main>
          <Header />
          <h1>{person.nomina}</h1>
          <div className="person-details">
            <section>
              <div>
                <h2>Basic Info</h2>
              </div>
              <p>Gender: {person.gender}</p>
              <p>Certainity of identification: {person.certainty_of_id}</p>
              <code>
                (Rating from 1-5, with 5 being agreement among scholars and 1
                being considerable confusion as to the person.)
              </code>
            </section>
            <section className="inline">
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
            <PersonDates
              hasDates={hasDates(person)}
              dates={{
                birth: person.birth,
                death: person.death,
                cos: person.cos,
                cos_suff: person.cos_suff,
                floruit: person.floruit,
              }}
            />
            <section>
              <div>
                <h2>Letters to</h2>
              </div>
              <ul>
                {person.letters_to.map((el, index) => (
                  <li key={index}>{el}</li>
                ))}
              </ul>
            </section>
            <section>
              <div>
                <h2>Citations</h2>
              </div>
              <ul className="vertical">
                {person.citations.map((el, index) => (
                  <li key={index} dangerouslySetInnerHTML={{ __html: el }}></li>
                ))}
              </ul>
            </section>
          </div>
        </main>
      </React.Fragment>
    );
  }

  static async getInitialProps({ res, req, query }: NextPageContext) {
    try {
      const baseUrl = getBaseUrl(req);
      const data = await axios.get(baseUrl + `/api/people/${query.id}`);
      const person = data.data;
      if (req && res) {
        if (req.url!.search(slugify(person.nomina)) === -1) {
          res.writeHead(302, {
            Location: `/people/${slugify(person.nomina)}-${query.id}`,
          });
          res.end();
        }
      }

      return {
        id: query.id,
        person: person,
      };
    } catch (err) {
      return {
        id: query.id,
        person: undefined,
      };
    }
  }
}

export default PersonDetail;
