import * as React from 'react';
import Router from 'next/router';
import axios from 'axios';
import { timeParse } from 'd3';

interface InputProps {
  placeholder?: string,
  name: string,
  id: string,
  action?: string,
  method?: string,
  label: string,
}

interface InputState {
  value: string,
  expanded: boolean,
  options: Array<string>,
  filteredOptions: Array<string>
}

export default class QuickSearch extends React.Component<InputProps, InputState> {
  constructor(props: InputProps) {
    super(props)
    this.state = {value: '', expanded: false, options: [], filteredOptions: []}

  }

  async componentDidMount() {
    try {
      const res = await axios.get('/api/people/autocomplete');
      const nomina: Array<string> = res.data.map((x: any) => x.nomina).sort();
        this.setState({options: nomina, filteredOptions: nomina})
    } catch(err) {
      this.setState({options: []})
    }

  }

  filterOptions = (value: string): {
    const temp = this.state.options.slice()
    this.setState({filteredOptions: temp.filter(x => x.startsWith(value))}
  }

  handleFocusInput = (event: React.FocusEvent<HTMLInputElement>): void => {
    this.setState({expanded: true})
  }

  handleSubmit = (event: React.FormEvent<HTMLFormElement>): void => {
    event.preventDefault()
    Router.push(`${this.props.action}?nomina=${this.state.value}`)
  }

  handleChange = (event: React.ChangeEvent<HTMLInputElement>): void => {
    event.preventDefault()
    this.setState({value: event.target.value})
  }

  render() {
    return (
      <form action={this.props.action} method={this.props.method} onSubmit={this.handleSubmit}>
        <label id={`label_${this.props.id}`} htmlFor={this.props.id}>{this.props.label}</label>
        <div className='combobox-wrapper'>
          <input type='text' aria-autocomplete="list" 
          aria-controls={`quicksearch-listbox-${this.props.id}`}
          aria-haspopup="listbox"
          aria-expanded={this.state.expanded}
          id={this.props.id} value={this.state.value} name={this.props.name}
          placeholder={this.props.placeholder} onChange={this.handleChange}
          onFocus={this.handleFocusInput}>
          </input>
        </div>
        <ul aria-labelledby={`label_${this.props.id}`} className={this.state.expanded ? '' : 'hidden'} 
        role="listbox" id={`quicksearch-listbox-${this.props.id}`}>
          {this.state.filteredOptions.map((el, index) =>
              <li key={index}>{el}</li>
            )}
        </ul>
      </form>
    )
  }
}
