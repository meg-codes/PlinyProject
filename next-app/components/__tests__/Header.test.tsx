/* eslint-env jest */
import { shallow, ShallowWrapper} from 'enzyme';

import ActiveLink from '../ActiveLink';
import QuickSearch from '../QuickSearch';
import Header from '../Header';

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