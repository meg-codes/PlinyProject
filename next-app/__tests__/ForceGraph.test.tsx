/* eslint-env jest */
import { shallow } from 'enzyme';

import ForceGraph from '../components/ForceGraph';

describe('ForceGraph', () => {
  it('renders an svg of the specified props', () => {
      const forcegraph = shallow(<ForceGraph height={300} width={300} title='test graph' id='test'/>)
      expect(forcegraph.render()).toMatchSnapshot();

  })
})