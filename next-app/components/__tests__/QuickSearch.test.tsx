/* eslint-env jest */
import { mount, ReactWrapper, shallow } from 'enzyme';
import MockAdapter from 'axios-mock-adapter';
import axios from 'axios';

import QuickSearch from '../QuickSearch';

describe('Quicksearch', () => {

  const mockData = [
    { nomina: "Cornelius Tacitus"},
    { nomina: 'L. Calpurnius Fabatus'},
    { nomina: "Novius Maximus"},
    { nomina: "Maturus Arrianus"}
  ]

  let mock: MockAdapter
  let quicksearch: ReactWrapper

  beforeEach(() => {
    mock = new MockAdapter(axios);
    mock
      .onGet("/api/people/autocomplete")
      .reply(200, mockData)
    quicksearch = mount(
      <QuickSearch id="test" 
      name="test_name" 
      label="Test Lookup"
      placeholder='enter to search'
      action='/api/post'
      method='POST'
      />);
  })

  it('should render based on an ajax call', done => {
    
    
    setTimeout(() => {
      quicksearch.update();
      expect(quicksearch.html()).toMatchSnapshot();
      done();
    });

  });

  it('should render list empty if ajax call fails', () => {
    mock.onGet('/api/people/autocomplete').reply(500)
    const dudSearch = shallow(<QuickSearch id='foo' name='bar' label='baz'></QuickSearch>)
    expect(dudSearch.html()).toMatchSnapshot()
  });

  it('should show combobox and respond to keypresses when input is focused', done => {
    
    const spy = jest.spyOn(quicksearch.instance(), 'setScroll')
    
    setTimeout(() => {
      quicksearch.setState({value: 't'})
      const input = quicksearch.find('input')
      input.simulate('focus');
      expect(quicksearch.state('expanded')).toBeTruthy();
      expect(quicksearch.find('.hidden')).toHaveLength(0);

      // select the first item
      input.simulate('keydown', {key: 'ArrowDown'})
      const focused = quicksearch.find('li.focused')
      expect(focused).toHaveLength(1)
      expect(focused.prop('aria-selected')).toBeTruthy()
      expect(quicksearch.state('focusedOption')).toBe(0)
      expect(spy).toBeCalled()

      // cycle to last item
      input.simulate('keydown', {key: 'ArrowUp'})
      expect(quicksearch.state('focusedOption')).toBe(3)
      expect(spy).toBeCalledTimes(2)
      
      // select an item
      input.simulate('keydown', {key: 'Enter'})
      expect(quicksearch.find('.hidden')).toHaveLength(1);
      expect(quicksearch.state('value')).toBe("Novius Maximus")      


      // esc clears input
      input.simulate('focus');
      input.simulate('keydown', {key: 'Escape'})
      expect(quicksearch.find('.hidden')).toHaveLength(1)
      expect(quicksearch.state('value')).toBe('')

      done();
    });
  });


});