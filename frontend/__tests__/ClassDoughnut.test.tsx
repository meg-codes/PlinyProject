/* eslint-env jest */
import { mount } from 'enzyme';
import axios from 'axios';
import MockAdapter from 'axios-mock-adapter';
import ClassDoughnut from '../components/ClassDoughnut';

import mockAllData from './__fixtures__/mockclassdata';
import mockbookData from './__fixtures__/mockclassdatabookone'

describe('ClassDoughnut', () => {

    let mock: MockAdapter

    beforeEach(() => {
      mock = new MockAdapter(axios);
      mock
        .onGet('/people/social_class.json')
        .reply(200, mockAllData)
      mock
        .onGet('/people/social_class.json?q=1')
        .reply(200, mockbookData);
    });

    it('should render initially with data from api', done => {
      const classdoughnut = mount(<ClassDoughnut></ClassDoughnut>);
      expect(classdoughnut.html()).toMatchSnapshot();
      setTimeout(() => {
        expect(classdoughnut.state('chartData')).toBeDefined();
        expect(classdoughnut.state('chart')).toBeDefined();
        done();
      });
    });

    it('should gracefully handle a network error', done => {
      mock.onGet('/people/social_class.json').reply(500);
      const classdoughnut = mount(<ClassDoughnut></ClassDoughnut>);
      setTimeout(() => {
        expect(classdoughnut.state('chartData')).toBeUndefined();
        expect(classdoughnut.state('chart')).toBeUndefined();
        done();
      });
    });

    it('should update when the user selects a book', done => {
      const classdoughnut = mount(<ClassDoughnut></ClassDoughnut>);
      const spy = jest.spyOn(axios, 'get');
      classdoughnut.find('select').simulate('change', {target: {value: 1}});
      setTimeout(() => {
        expect(classdoughnut.state('book')).toEqual(1);
        expect(spy).toHaveBeenLastCalledWith('/people/social_class.json?q=1');
        const chartData = classdoughnut.state('chartData');
        //@ts-ignore
        expect(chartData.datasets[0].data).toEqual([8, 10, 11])
        mock.onGet('/people/social_class.json').reply(500);
        classdoughnut.find('select').simulate('change', {target: {value: 'all'}});
        setTimeout(() => {
          expect(classdoughnut.state('book')).toBeUndefined();
          const chartDataNew = classdoughnut.state('chartData');
          //@ts-ignore
          expect(chartDataNew.datasets[0].data).toEqual([8, 10, 11]);
          done();
        });
      });
    });


});