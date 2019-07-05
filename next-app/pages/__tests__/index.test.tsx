/* eslint-env jest */
import { shallow } from 'enzyme';

import MockAdapter from 'axios-mock-adapter';
import axios from 'axios';
import Home from '../index';
import { Post, Posts } from '../index';
import { NextContext } from 'next';

const mockData:Post[] = [
  {
    id: 1,
    subject: 'test post',
    content: 'this is a test post',
    date_updated: new Date('2020-01-01')
  },
  {
    id: 2,
    subject: 'test post 2',
    content: 'this is a test post',
    date_updated: new Date('2020-01-02')
  }
]

let mock: MockAdapter

describe('Home', () => {

  beforeEach(() => {
    mock = new MockAdapter(axios);
  });

  it('should render posts passed as props', () => {
    const home = shallow(<Home posts={mockData}/>);
    expect(home.find(Posts).html()).toMatchSnapshot();
  });

  it('should use getInitialProps to make an API call without a request', () => {
    mock
      .onGet('/api/posts')
      .reply(200, mockData);
    expect.assertions(1);
    return Home.getInitialProps({req: undefined} as NextContext)
    .then(posts => expect(posts).toEqual({posts: mockData}));
  });

  it('should use getInitial props to make an API call with a request', () => {
    mock
      .onGet('http://localhost:3000/api/posts')
      .reply(200, mockData);
    expect.assertions(1);
    return Home.getInitialProps(
        {
          req: {
            protocol: 'http',
            get: (prop: string) => {
              if ((prop) === 'Host') return 'localhost:3000'
            }
          }
        } as unknown as NextContext
      ).then(posts => expect(posts).toEqual({posts: mockData}));    
  });

  it('should return an empty array on network error', () => {
    mock
      .onGet('/api/posts')
      .reply(500)
    expect.assertions(1)
    return Home.getInitialProps({req: undefined} as NextContext)
      .then(posts => expect(posts).toEqual({posts: []}))
  });
});

