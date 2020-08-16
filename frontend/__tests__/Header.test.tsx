/* eslint-env jest */
import { shallow, ShallowWrapper} from 'enzyme';

import ActiveLink from '../components/ActiveLink';
import QuickSearch from '../components/QuickSearch';
import Header from '../components/Header';

describe('Header', () => {

  let header: ShallowWrapper;

  beforeAll(() => {
    header = shallow(<Header></Header>);
  })

  it('should have four active links', () =>{
    expect(header.find(ActiveLink)).toHaveLength(4);
  });

  it('should render q QuickSearch component', () => {
    expect(header.find(QuickSearch)).toHaveLength(1);
  });

});