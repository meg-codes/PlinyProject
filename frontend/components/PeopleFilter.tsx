import * as React from "react";
import Router from "next/router";
import { ParsedUrlQuery } from "querystring";

interface PeopleFilterProps {
  query: ParsedUrlQuery;
}

interface PeopleFilterState {
  nomina?: string;
  senatorial: boolean;
  equestrian: boolean;
  citizen: boolean;
  [key: string]: any;
}

function filterStateToString(state: PeopleFilterState) {
  const queryString: Array<string> = [];

  for (let prop in state) {
    if (prop == "nomina" && state.nomina) {
      queryString.push(`nomina=${state.nomina}`);
    } else {
      if (state[prop]) {
        queryString.push(`socialClass=${prop}`);
      }
    }
  }
  return queryString.length > 0 ? `?${queryString.join("&")}` : "";
}

export default class PeopleFilter extends React.Component<
  PeopleFilterProps,
  PeopleFilterState
> {
  constructor(props: PeopleFilterProps) {
    super(props);

    const socialClasses = this.props.query.socialClass;
    const tempState: PeopleFilterState = {
      nomina: (this.props.query.nomina as string) || "",
      senatorial: false,
      equestrian: false,
      citizen: false,
    };
    if (
      socialClasses &&
      Array.isArray(socialClasses) &&
      socialClasses.length > 0
    ) {
      socialClasses.forEach((el) => {
        tempState[el] = true;
      });
    }

    if (typeof socialClasses == "string") {
      tempState[socialClasses] = true;
    }

    this.state = tempState;
  }

  submit = (): void => {
    const queryString = filterStateToString(this.state);
    Router.push(`/people${queryString}`);
  };

  handleSubmit = (event: React.FormEvent<HTMLFormElement>): void => {
    event.preventDefault();
    this.submit();
  };

  handleValueChange = (event: React.ChangeEvent<HTMLInputElement>): void => {
    event.preventDefault();
    this.setState({ nomina: event.target.value });
  };

  handleCheckedChange = (event: React.ChangeEvent<HTMLInputElement>): void => {
    event.preventDefault();
    this.setState({ [event.target.value]: event.target.checked }, this.submit);
  };

  render() {
    return (
      <form id="people-form" action="/people" onSubmit={this.handleSubmit}>
        <label htmlFor="nomina">Nomina</label>
        <input
          type="text"
          id="nomina"
          name="nomina"
          value={this.state.nomina}
          onChange={this.handleValueChange}
        />
        <fieldset name="socialClass">
          <legend>Ordo (Social Class) Filters</legend>
          <input
            type="checkbox"
            id="socialClass_1"
            name="socialClass"
            value="citizen"
            checked={this.state.citizen}
            onChange={this.handleCheckedChange}
          />
          <label htmlFor="socialClass_1">Citizen</label>

          <input
            type="checkbox"
            id="socialClass_2"
            name="socialClass"
            value="equestrian"
            checked={this.state.equestrian}
            onChange={this.handleCheckedChange}
          />
          <label htmlFor="socialClass_2">Equestrian</label>
          <input
            type="checkbox"
            id="socialClass_3"
            name="socialClass"
            value="senatorial"
            checked={this.state.senatorial}
            onChange={this.handleCheckedChange}
          />
          <label htmlFor="socialClass_3">Senatorial</label>
        </fieldset>
      </form>
    );
  }
}
