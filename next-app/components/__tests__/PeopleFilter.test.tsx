/* eslint-env jest */
import { shallow } from 'enzyme';
import { QueryStringMapObject } from 'next';

jest.mock('next/router');
import Router from 'next/router';

import PeopleFilter from '../PeopleFilter';


describe('PeopleFilter', () => {
  const querymap = {
    nomina: 'Tacitus',
    socialClass: ['senatorial', 'equestrian']
  }

  it('accepts a query map as props', () => {

    let peoplefilter = shallow(<PeopleFilter query={querymap}/>)
    expect(peoplefilter.state('nomina')).toBe('Tacitus');
    expect(peoplefilter.state('senatorial')).toBeTruthy();
    expect(peoplefilter.state('equestrian')).toBeTruthy()
    expect(peoplefilter.state('citizen')).toBeFalsy()

    // test a single social class and no nomina
    const newQueryMap = {
      socialClass: 'citizen'
    }
    peoplefilter = shallow(<PeopleFilter query={newQueryMap}/>);
    expect(peoplefilter.state('nomina')).toBe('');
    expect(peoplefilter.state('citizen')).toBeTruthy();
    expect(peoplefilter.state('equestrian')).toBeFalsy();
    expect(peoplefilter.state('sentatorial')).toBeFalsy();
  });

  it('should serialize its state to querystring on submit', () => {

    const peoplefilter = shallow(<PeopleFilter query={querymap} />);
    peoplefilter.find('form').simulate('submit', {preventDefault: jest.fn()});
    expect(Router.push).toHaveBeenCalledWith('/people?nomina=Tacitus&socialClass=senatorial&socialClass=equestrian')
    
  });

  it('should change its state on nomina changing', () => {
    
    const peoplefilter = shallow(<PeopleFilter query={querymap} />);
    peoplefilter.find('#nomina').simulate('change', {
      preventDefault: jest.fn(), 
      target:{ value: 'foobar'}
    });
    expect(peoplefilter.state('nomina')).toBe('foobar');
  });

  it('should change its state on checkboxes being selected', () => {
    const peoplefilter = shallow(<PeopleFilter query={querymap} />);
    peoplefilter.find('#socialClass_2').simulate('change', {
      preventDefault: jest.fn(),
      target: {checked: true}
    });
    peoplefilter.find('#socialClass_3').simulate('change', {
      preventDefault: jest.fn(),
      target: {checked: true}
    });
    expect(peoplefilter.state('senatorial')).toBeTruthy();
    expect(peoplefilter.state('equestrian')).toBeTruthy();
    expect(peoplefilter.state('citizen')).toBeFalsy();

  });
});
