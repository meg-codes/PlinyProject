import * as React from 'react';
import Router from 'next/router';

interface InputProps {
  placeholder?: string,
  name: string,
  id: string,
  action?: string,
  method?: string,
  label: string
}

interface InputState {
  value: string
}

export default class QuickSearch extends React.Component<InputProps, InputState> {
  constructor(props: InputProps) {
    super(props)
    this.state = {value: ''}

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
        <label htmlFor={this.props.id}>{this.props.label}</label>
        <input type='text' id={this.props.id} value={this.state.value} name={this.props.name}
        placeholder={this.props.placeholder} onChange={this.handleChange}>
        </input>
      </form>
    )
  }
}
