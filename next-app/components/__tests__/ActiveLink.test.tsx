/* eslint-env jest */
import { shallow } from 'enzyme';

import { ActiveLink } from '../ActiveLink'

describe('ActiveLink', () => {

  const router: any = {
    pathname: '/'
  }

  it('renders a link based on its href', () => {
    
    const activelink = shallow(<ActiveLink href='/home/' router={router}><a>Home</a></ActiveLink>)
    expect(activelink.find('[href="/home/"]')).toHaveLength(1)
    // not set to active
    expect(activelink.find('.active')).toHaveLength(0)
  });

  it('renders a link as active if the href matches pathname', () => {
    const activelink = shallow(<ActiveLink href='/' router={router}><a>Home</a></ActiveLink>)
    expect(activelink.find('[href="/"]')).toHaveLength(1)
    // set to active
    expect(activelink.find('.active')).toHaveLength(1)
  });


});