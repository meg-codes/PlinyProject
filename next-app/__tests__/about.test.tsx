/* eslint-env jest */
import { shallow } from 'enzyme'

jest.mock('../components/Header');
import Header from '../components/Header';
import About from '../pages/about';


(Header as jest.Mock).mockReturnValue(<head></head>)

describe('about', () => {
  it('should render correctly to display info', () => {
    const about = shallow(<About/>);
    expect(about.html()).toMatchSnapshot();
  });
});