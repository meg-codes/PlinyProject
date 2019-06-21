import * as React from 'react';
import { withRouter, WithRouterProps } from "next/router";
import Link from 'next/link';
import { LinkProps } from 'next/link';

interface ActiveLinkProps extends WithRouterProps, LinkProps {}

const ActiveLink:React.FC<ActiveLinkProps> = ({ children, router, href, ...props}) => (
  <Link href={href} {...props}>
    {React.cloneElement(React.Children.only(children), {
      className: href === router.pathname ? `active` : null
    })}
  </Link>
)

export default withRouter(ActiveLink)
