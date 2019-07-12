/* eslint-env jest */
import { shallow, mount } from 'enzyme';
import axios from 'axios';
import MockAdapter from 'axios-mock-adapter';
import ClassDoughnut from '../ClassDoughnut';

import mockAllData from './__fixtures__/mockclassdata';
import mockbookData from './__fixtures__/mockclassdatabookone'

describe('ClassDoughnut', () => {

    let mock: MockAdapter

    beforeEach(() => {
      mock = new MockAdapter(axios);
      mock
        .onGet('/people/social_class.json')
        .reply((config) => {
          if (config.params && config.params.q && config.params.q === "1") {
            return [200, mockbookData];
          } else if (config.params && config.params.q && config.params.q === "2") {
            return [500];
          }

          return [200, mockAllData];

        });
    });

    it('should render initially with data from api', done => {
      const classdoughnut = mount(<ClassDoughnut></ClassDoughnut>);
      expect(classdoughnut.html()).toMatchSnapshot();
      setTimeout(() => {
        expect(classdoughnut.state('data')).toBeDefined();
        done();
      });
    });

})